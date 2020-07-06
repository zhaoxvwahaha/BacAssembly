hybrid assembly pipeline for bacteria
Standard Readme
standard-readme compliant

A standard style for README files

Your README file is normally the first entry point to your code. It should tell people why they should use your module, how they can install it, and how they can use it. Standardizing how you write your README makes creating and maintaining your READMEs easier. Great documentation takes work!

This repository contains:

The specification for how a standard README should look.
A link to a linter you can use to keep your README maintained (work in progress).
A link to a generator you can use to create standard READMEs.
A badge to point to this spec.
Examples of standard READMEs - such as this file you are reading.
Standard Readme is designed for open source libraries. Although it’s historically made for Node and npm projects, it also applies to libraries in other languages and package managers.

Table of Contents
Background
Install
Usage
Generator
Badge
Example Readmes
Related Efforts
Maintainers
Contributing
License
Background
Standard Readme started with the issue originally posed by @maxogden over at feross/standard in this issue, about whether or not a tool to standardize readmes would be useful. A lot of that discussion ended up in zcei's standard-readme repository. While working on maintaining the IPFS repositories, I needed a way to standardize Readmes across that organization. This specification started as a result of that.

Your documentation is complete when someone can use your module without ever having to look at its code. This is very important. This makes it possible for you to separate your module's documented interface from its internal implementation (guts). This is good because it means that you are free to change the module's internals as long as the interface remains the same.

Remember: the documentation, not the code, defines what a module does.

~ Ken Williams, Perl Hackers

Writing READMEs is way too hard, and keeping them maintained is difficult. By offloading this process - making writing easier, making editing easier, making it clear whether or not an edit is up to spec or not - you can spend less time worrying about whether or not your initial documentation is good, and spend more time writing and using code.

By having a standard, users can spend less time searching for the information they want. They can also build tools to gather search terms from descriptions, to automatically run example code, to check licensing, and so on.

The goals for this repository are:

A well defined specification. This can be found in the Spec document. It is a constant work in progress; please open issues to discuss changes.
An example README. This Readme is fully standard-readme compliant, and there are more examples in the example-readmes folder.
A linter that can be used to look at errors in a given Readme. Please refer to the tracking issue.
A generator that can be used to quickly scaffold out new READMEs. See generator-standard-readme.
A compliant badge for users. See the badge.
Install
This project uses node and npm. Go check them out if you don't have them locally installed.

$ npm install --global standard-readme-spec
Usage
This is only a documentation package. You can print out spec.md to your console:

$ standard-readme-spec
# Prints out the standard-readme spec
Generator
To use the generator, look at generator-standard-readme. There is a global executable to run the generator in that package, aliased as standard-readme.

Badge
If your README is compliant with Standard-Readme and you're on GitHub, it would be great if you could add the badge. This allows people to link back to this Spec, and helps adoption of the README. The badge is not required.

standard-readme compliant

To add in Markdown format, use this code:

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)
Example Readmes
To see how the specification has been applied, see the example-readmes.

Related Efforts
Art of Readme - 💌 Learn the art of writing quality READMEs.
open-source-template - A README template to encourage open-source contributions.
Maintainers
@RichardLitt.

Contributing
Feel free to dive in! Open an issue or submit PRs.

Standard Readme follows the Contributor Covenant Code of Conduct.

Contributors
This project exists thanks to all the people who contribute. 

License
MIT © Richard Littauer
