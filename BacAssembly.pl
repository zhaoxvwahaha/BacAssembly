#! /usr/bin/perl -w
use strict;
use Getopt::Long;
use File::Spec;
use POSIX qw(strftime);
use FindBin qw($Bin);
use File::Path;

my $usage="Pipeline for hybrid assembly using short and long reads
    Usage:
    Options:
        -i <input>  input txt_file contain 4 cols (sample_ID Path2raw.Long_reads.fq.gz Path2raw.short_readas.1.fq.gz Path2raw.short_readas.2.fq.gz )
        -c <config> configure file
        -o <opath> output path [./result]
        -h|?Help!
    Example:Perl $0 -i data.info -c cfg.file
";

my ($input,$cfg,$outpath,$help);
GetOptions(
    '-i=s' => \$input,
    '-c=s' => \$cfg,
    '-o=s' => \$outpath,
    'h|?'=> \$help,
);  
if ($help or !$input){die "$usage\n";}

#$outpath ||= "./result";
$outpath ||= "./";
mkdir ("$outpath") unless (-d $outpath);
$outpath=File::Spec->rel2abs($outpath);
my $shellall="$outpath/shellall";
mkdir ($shellall) unless (-d $shellall);

### read config file ###
print strftime(">>>Generate shell scripts started at:%Y-%m-%d,%H:%M:%S\n\n",localtime(time));
my %config= &readConf($cfg);

sub readConf{
    my $confFile=shift @_;
    my %hash;
    open IN,$confFile or die "Can't open file $confFile:$!\n";
    while (<IN>){
        chomp;
	next if(/^\s*$/ || /^\s*\#/);
        $_ =~ s/^\s*//;
        $_ =~ s/#(.)*//;
        $_ =~ s/\s*$//;
        if (/^(\w+)\s*=\s*(.*)$/xms){
            next if ($2 =~ /^\s*$/);
            my $key = $1; 
            my $value = $2; 
            $value =~ s/\s*$//;
            $hash{$key} = $value;
        }
    }   
    return %hash;
}
        


### read input data list ###
my %data;
my $dataNum;
my %sample;
my @sample;
open LIST,"$input" or die $!;
#open NP,">$outpath/input.np" or die $!;
while (<LIST>){
	chomp;
	next if (/^#/);
	my ($name,$lpath,$spath1,$spath2)=(split/\s+/,$_)[0,1,2,3];
	$lpath=File::Spec->rel2abs($lpath);
	$spath1=File::Spec->rel2abs($spath1);
	$spath2=File::Spec->rel2abs($spath2);
	$data{$name}="$lpath $spath1 $spath2";
#	print NP "$name\t$lpath\t$spath1\t$spath2\n";
	push @sample,$name;
	$dataNum++;
}
close LIST;

my @dependent;

###01.porechop
if ($config{Lreads_adapter_method} eq "porechop"){
	my $outdir="$outpath/result/01.porechop";
	mkpath ($outdir) unless (-d $outdir);
	open SH, ">$shellall/01.porechop.sh" or dir $!;
	foreach my $name (@sample){
		mkdir ("$outdir/$name") unless (-d "$outdir/$name");
		my $lpath=(split /\s+/,$data{$name})[0];
#		print SH "$config{'porechop'} $config{'porechop_Parameters'} -i $lpath -o $outdir/$name/$name.porechop.reads.fq >$outdir/$name/$name.porechop.log && \n"; 
		print SH "$config{'porechop'} -i $lpath -o $outdir/$name/$name.porechop.reads.fq >$outdir/$name/$name.porechop.log\n";
	}
	close SH;
} 

###02.NanoFilt+NanoStat
if ($config{Lreads_filt_method} eq "NanoFilt"){
	my $outdir="$outpath/result/02.NanoFilt";
	mkpath ($outdir) unless (-d $outdir);
	open SH, ">$shellall/02.nanofilt.sh" or dir $!;
	foreach my $name (@sample){
		mkdir ("$outdir/$name") unless (-d "$outdir/$name");
		print SH "$config{'nanofilt'} $config{'nanofilt_Parameters'} --logfile $outdir/$name/$name.nanofilt.log $outpath/01.porechop/$name/$name.porechop.reads.fq |gzip >$outdir/$name/$name.nanofilt.fq.gz && $config{'nanostat'} --fastq $outdir/$name/$name.nanofilt.fq.gz >$outdir/$name/$name.nanofilt.fq.gz.nanostat\n";
	}
	close SH;
} 
		
###01_2.short.clean.reads:fastp+soapnuke
if ($config{Sreads_filt_method} eq "fastp+soapnuke"){
	my $outdir="$outpath/result/01_2.short.clean.reads";
	mkpath ($outdir) unless (-d $outdir);
	open SH,">$shellall/01_2.short.clean.reads.sh" or dir $!;
	foreach my $name(@sample){
		mkdir ("$outdir/$name") unless (-d "$outdir/$name");
		my ($path1,$path2)=(split /\s+/,$data{$name})[1,2];
		print SH "$config{'fastp'} $config{'fastp_Parameters'} -i $path1 -o $outdir/$name/$name.fastp.clean.1.fa.gz -I $path2 -O $outdir/$name/$name.fastp.clean.2.fa.gz -j $outdir/$name/$name.fastp.json -h $outdir/$name/$name.fastp.html -R $name && $config{'soapnuke'} $config{'soapnuke_Parameters'} -1 $outdir/$name/$name.fastp.clean.1.fq.gz -2 $outdir/$name/$name.fastp.clean.2.fq.gz -C $name.fastp.nodup.clean.1.fq.gz -D $name.fastp.nodup.clean.2.fq.gz -o $outdir/$name\n";
	}
	close SH;
}	
###03.flye
if ($config{Lreads_assembly_method} eq "flye"){
	my $outdir="$outpath/result/03.flye";
	mkpath ($outdir) unless (-d $outdir);
	open SH,">$shellall/03.flye.sh" or dir $!;
	foreach my $name(@sample){
		mkdir ("$outdir/$name") unless (-d "$outdir/$name");
		print SH "$config{'flye'} $config{'flye_Parameters'} $outpath/02.NanoFilt/$name/$name.nanofilt.fq.gz -o $outdir/$name\n";
	}
	close SH;
}
###04.racon
if ($config{'Lreads_1st_polish_method'} eq "racon"){
	my $outdir="$outpath/result/04.racon";
	mkpath ($outdir) unless (-d $outdir);
	open SH,">$shellall/04.racon.sh" or dir $!;
	foreach my $name(@sample){
		mkdir ("$outdir/$name") unless (-d "$outdir/$name");
		print SH "$config{'bwa'} index $outpath/03.flye/$name/assembly.fasta\n$config{'bwa'} mem $outpath/03.flye/$name/assembly.fasta $outpath/02.NanoFilt/$name/$name.nanofilt.fq.gz >$outdir/$name/$name.sam\n$config{'racon'} $config{'racon_Parameters'} $outpath/02.NanoFilt/$name/$name.nanofilt.fq.gz $outpath/03.flye/$name/assembly.fasta >$outdir/$name/$name.racon.fasta\n";
	}
	close SH;
}

###05.medaka
if ($config{'Lreads_2nd_polish_method'} eq "medaka"){
	my $outdir="$outpath/result/05.medaka";
	mkpath ($outdir) unless (-d $outdir);
	open SH,">$shellall/05.medaka.sh" or dir $!;
	foreach my $name (@sample){
		mkdir ("$outdir/$name") unless (-d "$outdir/$name");
		print SH "$config{'medaka'} $config{'medaka_Parameters'} -i $outpath/02.NanoFilt/$name/$name.nanofilt.fq.gz -d $outpath/04.racon/$name/$name.racon.fasta -o $outdir/$name\n";
	}
	close SH;
}
###06.pilon
if ($config{'Sreads_polish_method'} eq "pilon"){
	my $outdir="$outpath/result/06.pilon";
	mkpath ($outdir) unless (-d $outdir);
	open SH,">$shellall/06.pilon.sh" or dir $!;
	foreach my $name (@sample){
		mkdir ("$outdir/$name") unless (-d "$outdir/$name");
		print SH "java -Xmx32G -jar $config{'pilon'} $config{'pilon_Parameters'} --genome $outpath/05.medaka/$name/consensus.fasta --frags $outdir/$name/mapping.sorted.bam --outdir $outdir/$name --output $name\n";
	}
	close SH;
}

###07.circlator
if ($config{'Lreads_circlator_method'} eq "circlator"){
	my $outdir="$outpath/result/07.circlator";
	mkpath ($outdir) unless (-d $outdir);
	open SH,">$shellall/07.circlator.sh" or dir $!;
	foreach my $name (@sample){
		mkdir ("$outdir/$name") unless (-d "$outdir/$name");
		print SH "$config{'circlator'} $config{circlator_Parameters} $outpath/06.pilon/$name/$name.fasta $outpath/02.NanoFilt/$name/$name.nanofilt.fq.gz $outdir/$name\n";
	}
	close SH;
}
###03_2.unicycler
if ($config{'Sreads_first_assembly_method'} eq "unicycler"){
	my $outdir="$outpath/result/03_2.unicycler";
	mkpath ($outdir) unless (-d $outdir);
	open SH,">$shellall/03_2.unicycler.sh" or dir $!;
	foreach my $name (@sample){
		mkdir ("$outdir/$name") unless (-d "$outdir/$name");
		my ($lpath,$spath1,$spath2)=(split /\s+/,$data{$name})[0,1,2];
		print SH "$config{'unicycler'} $config{unicycler_Parameters} -1 $spath1 -2 $spath2 -l $lpath -o $outdir/$name\n";
	}
	close SH;
}



