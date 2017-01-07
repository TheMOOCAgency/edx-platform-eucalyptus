
Pa11y JSON Reporter for Old Node
================================

A reporter for [Pa11y][pa11y] which outputs JSON in the 2.0 format, but without
using the [`bfj`](https://github.com/philbooth/bfj) module.

[![NPM version][shield-npm]][info-npm]
[![Node.js version support][shield-node]][info-node]
[![Build status][shield-build]][info-build]
[![Dependencies][shield-dependencies]][info-dependencies]
[![GPLv3 licensed][shield-license]][info-license]

```sh
pa11y --reporter json-oldnode nature.com
```


Usage
-----

Install Pa11y and this project with [npm][npm]:

```
npm install -g pa11y
npm install -g pa11y-reporter-json-oldnode
```

Use the reporter with the `--reporter` flag:

```sh
pa11y --reporter json-oldnode nature.com
```

You'll get the JSON output as using `--reporter json`!


Contributing
------------

To contribute to Pa11y JSON Reporter for Old Node,
clone this repo locally and commit your code on a separate branch.

Please check that everything works by running the following before opening a pull-request:

```sh
make ci
```


License
-------

Pa11y JSON Reporter for Old Node is licensed under the [Lesser General Public License (LGPL-3.0)][info-license].


[npm]: https://www.npmjs.com/
[pa11y]: https://github.com/pa11y/pa11y

[info-dependencies]: https://gemnasium.com/singingwolfboy/pa11y-reporter-json-oldnode
[info-license]: LICENSE
[info-node]: package.json
[info-npm]: https://www.npmjs.com/package/pa11y-reporter-json-oldnode
[info-build]: https://travis-ci.org/singingwolfboy/pa11y-reporter-json-oldnode
[shield-dependencies]: https://img.shields.io/gemnasium/singingwolfboy/pa11y-reporter-json-oldnode
[shield-license]: https://img.shields.io/badge/license-LGPL%203.0-blue.svg
[shield-node]: https://img.shields.io/node/v/pa11y-reporter-json-oldnode.svg?label=node.js%20support
[shield-npm]: https://img.shields.io/npm/v/pa11y-reporter-json-oldnode.svg
[shield-build]: https://img.shields.io/travis/singingwolfboy/pa11y-reporter-json-oldnode/master.svg
