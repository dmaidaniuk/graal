#
# Copyright (c) 2018, Oracle and/or its affiliates. All rights reserved.
# DO NOT ALTER OR REMOVE COPYRIGHT NOTICES OR THIS FILE HEADER.
#
# The Universal Permissive License (UPL), Version 1.0
#
# Subject to the condition set forth below, permission is hereby granted to any
# person obtaining a copy of this software, associated documentation and/or
# data (collectively the "Software"), free of charge and under any and all
# copyright rights in the Software, and any and all patent rights owned or
# freely licensable by each licensor hereunder covering either (i) the
# unmodified Software as contributed to or provided by such licensor, or (ii)
# the Larger Works (as defined below), to deal in both
#
# (a) the Software, and
#
# (b) any piece of software and/or hardware listed in the lrgrwrks.txt file if
# one is included with the Software each a "Larger Work" to which the Software
# is contributed by such licensors),
#
# without restriction, including without limitation the rights to copy, create
# derivative works of, display, perform, and distribute the Software and make,
# use, sell, offer for sale, import, export, have made, and have sold the
# Software and the Larger Work(s), and to sublicense the foregoing rights on
# either these or other terms.
#
# This license is subject to the following condition:
#
# The above copyright notice and either this complete permission notice or at a
# minimum a reference to the UPL must be included in all copies or substantial
# portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
suite = {
  "mxversion" : "5.189.0",
  "name" : "truffle",
  "version" : "1.0.0-rc12",
  "release" : False,
  "groupId" : "org.graalvm.truffle",
  "sourceinprojectwhitelist" : [],
  "url" : "http://openjdk.java.net/projects/graal",
  "developer" : {
    "name" : "Truffle and Graal developers",
    "email" : "graal-dev@openjdk.java.net",
    "organization" : "Graal",
    "organizationUrl" : "https://github.com/oracle/graal",
  },
  "scm" : {
    "url" : "https://github.com/oracle/graal/tree/master/truffle",
    "read" : "https://github.com/oracle/graal.git",
    "write" : "git@github.com:oracle/graal.git",
  },
  "defaultLicense" : "UPL",
  "imports" : {
    "suites": [
      {
        "name" : "sdk",
        "subdir": True,
        "urls" : [
          {"url" : "https://curio.ssw.jku.at/nexus/content/repositories/snapshots", "kind" : "binary"},
         ]
      },
    ]
  },
  "libraries" : {

    # ------------- Libraries -------------

    "JLINE" : {
      "sha1" : "fdedd5f2522122102f0b3db85fe7aa563a009926",
      "maven" : {
        "groupId" : "jline",
        "artifactId" : "jline",
        "version" : "2.14.5",
      }
    },

    "LIBFFI" : {
      "urls" : [
        "https://lafo.ssw.uni-linz.ac.at/pub/graal-external-deps/libffi-3.2.1.tar.gz",
        "ftp://sourceware.org/pub/libffi/libffi-3.2.1.tar.gz",
      ],
      "sha1" : "280c265b789e041c02e5c97815793dfc283fb1e6",
    },

    "ANTLR4": {
      "sha1" : "946f8aa9daa917dd81a8b818111bec7e288f821a",
      "maven" : {
        "groupId" : "org.antlr",
        "artifactId" : "antlr4-runtime",
        "version" : "4.7.1",
      }
    },

    "ANTLR4_COMPLETE": {
      "urls": [
        "https://lafo.ssw.uni-linz.ac.at/pub/graal-external-deps/antlr-4.7.1-complete.jar",
        "http://www.antlr.org/download/antlr-4.7.1-complete.jar"
      ],
      "sha1": "90aa8308da72ae610207d8f6ca27736921be692a",
    },
  },
  "snippetsPattern" : ".*(Snippets|doc-files).*",
  "projects" : {

    # ------------- Truffle -------------

    "com.oracle.truffle.api" : {
      "subDir" : "src",
      "sourceDirs" : ["src"],
      "dependencies" : [
        "sdk:GRAAL_SDK",
      ],
      "uses" : [
        "com.oracle.truffle.api.TruffleRuntimeAccess",
        "java.nio.file.spi.FileTypeDetector",
      ],
      "exports" : [
        "<package-info>", # exports all packages containing package-info.java
        "com.oracle.truffle.api.impl", # exported to the Graal compiler
      ],
      "javaCompliance" : "8+",
      "checkstyleVersion" : "8.8",
      "workingSets" : "API,Truffle",
    },

    "com.oracle.truffle.api.utilities" : {
      "subDir" : "src",
      "sourceDirs" : ["src"],
      "dependencies" : [
        "com.oracle.truffle.api"
      ],
      "exports" : [
        "<package-info>", # exports all packages containing package-info.java
      ],
      "checkstyle" : "com.oracle.truffle.api",
      "javaCompliance" : "8+",
      "workingSets" : "API,Truffle",
    },

    "com.oracle.truffle.polyglot" : {
      "subDir" : "src",
      "sourceDirs" : ["src"],
      "uses" : ["com.oracle.truffle.api.impl.TruffleLocator",],
      "dependencies" : [
        "sdk:GRAAL_SDK",
        "com.oracle.truffle.api.instrumentation",
        "com.oracle.truffle.api.interop",
        "com.oracle.truffle.api.utilities",
      ],
      "exports" : [
        "<package-info>", # exports all packages containing package-info.java
      ],
      "forceJavac" : "true",
      "annotationProcessors" : ["TRUFFLE_DSL_PROCESSOR_INTEROP_INTERNAL"],
      "checkstyle" : "com.oracle.truffle.api",
      "javaCompliance" : "8+",
      "workingSets" : "API,Truffle",
    },

    "com.oracle.truffle.api.test" : {
      "subDir" : "src",
      "sourceDirs" : ["src"],
      "dependencies" : [
        "com.oracle.truffle.api.profiles",
        "com.oracle.truffle.api.interop",
        "com.oracle.truffle.api.debug",
        "com.oracle.truffle.api.utilities",
        "com.oracle.truffle.object.basic",
        "com.oracle.truffle.polyglot",
        "mx:JUNIT",
      ],
      "imports" : ["jdk.internal.loader"],
      "checkstyle" : "com.oracle.truffle.dsl.processor",
      "javaCompliance" : "8+",
      "annotationProcessors" : ["TRUFFLE_DSL_PROCESSOR"],
      "workingSets" : "API,Truffle,Test",
      "jacoco" : "exclude",
    },

    "com.oracle.truffle.api.benchmark" : {
      "subDir" : "src",
      "sourceDirs" : ["src"],
      "dependencies" : [
        "TRUFFLE_API",
        "TRUFFLE_INSTRUMENT_TEST",
        "mx:JMH_1_21",
      ],
      "imports" : ["jdk.internal.loader"],
      "checkstyle" : "com.oracle.truffle.dsl.processor",
      "javaCompliance" : "8+",
      "findbugsIgnoresGenerated" : True,
      "testProject" : True,
      "annotationProcessors" : ["mx:JMH_1_21", "TRUFFLE_DSL_PROCESSOR"],
      "workingSets" : "API,Truffle,Test",
      "jacoco" : "exclude",
    },

    "com.oracle.truffle.api.dsl" : {
      "subDir" : "src",
      "sourceDirs" : ["src"],
      "dependencies" : ["com.oracle.truffle.api"],
      "exports" : [
        "<package-info>", # exports all packages containing package-info.java
      ],
      "checkstyle" : "com.oracle.truffle.api",
      "javaCompliance" : "8+",
      "workingSets" : "API,Truffle,Codegen",
    },

    "com.oracle.truffle.api.dsl.test" : {
      "subDir" : "src",
      "sourceDirs" : ["src"],
      "dependencies" : [
        "com.oracle.truffle.dsl.processor",
        "com.oracle.truffle.polyglot",
        "com.oracle.truffle.api.test",
        "mx:JUNIT",
      ],
      "checkstyle" : "com.oracle.truffle.dsl.processor",
      "javaCompliance" : "8+",
      "annotationProcessors" : ["TRUFFLE_DSL_PROCESSOR"],
      "workingSets" : "API,Truffle,Codegen,Test",
      "jacoco" : "exclude",
    },

    "com.oracle.truffle.sl.tck" : {
      "subDir" : "src",
      "sourceDirs" : ["src"],
      "dependencies" : [
        "mx:JUNIT",
        "sdk:POLYGLOT_TCK"
      ],
      "exports" : [
        "com.oracle.truffle.sl.tck",
      ],
      "checkstyle" : "com.oracle.truffle.sl",
      "javaCompliance" : "8+",
      "workingSets" : "SimpleLanguage,Test",
    },

    "com.oracle.truffle.dsl.processor" : {
      "subDir" : "src",
      "sourceDirs" : ["src"],
      "dependencies" : [
        "com.oracle.truffle.api.dsl",
        "com.oracle.truffle.api.instrumentation",
        "truffle:ANTLR4"
      ],
      "checkstyle" : "com.oracle.truffle.dsl.processor",
      "javaCompliance" : "8+",
      "checkstyleVersion" : "8.8",
      "imports" : [
        "com.sun.tools.javac.processing",
        "com.sun.tools.javac.model",
        "com.sun.tools.javac.util",
        "com.sun.tools.javac.tree",
        "com.sun.tools.javac.file",
      ],
      "workingSets" : "Truffle,Codegen",
    },

    "com.oracle.truffle.dsl.processor.jdk9" : {
      "subDir" : "src",
      "sourceDirs" : ["src"],
      "dependencies" : [
        "com.oracle.truffle.dsl.processor",
      ],
      "checkstyle" : "com.oracle.truffle.dsl.processor",
      "javaCompliance" : "9+",
      "multiReleaseJarVersion" : "9",
      "imports" : [
        "com.sun.tools.javac.processing",
        "com.sun.tools.javac.model",
        "com.sun.tools.javac.util",
        "com.sun.tools.javac.tree",
        "com.sun.tools.javac.file",
      ],
      "workingSets" : "Truffle,Codegen",
    },

    "com.oracle.truffle.dsl.processor.interop" : {
      "subDir" : "src",
      "sourceDirs" : ["src"],
      "dependencies" : [
        "com.oracle.truffle.api.interop",
        "com.oracle.truffle.dsl.processor"
      ],
      "checkstyle" : "com.oracle.truffle.dsl.processor",
      "javaCompliance" : "8+",
      "imports" : [
        "com.sun.tools.javac.processing",
        "com.sun.tools.javac.model",
        "com.sun.tools.javac.util",
        "com.sun.tools.javac.tree",
        "com.sun.tools.javac.file",
      ],
      "workingSets" : "Truffle,Codegen",
    },

    "com.oracle.truffle.api.interop" : {
      "subDir" : "src",
      "sourceDirs" : ["src"],
      "dependencies" : [
        "com.oracle.truffle.api.dsl",
        "com.oracle.truffle.api.profiles",
      ],
      "annotationProcessors" : ["TRUFFLE_DSL_PROCESSOR_INTERNAL"],
      "exports" : [
        "<package-info>", # exports all packages containing package-info.java
      ],
      "checkstyle" : "com.oracle.truffle.api",
      "javaCompliance" : "8+",
      "workingSets" : "API,Truffle",
    },

   "com.oracle.truffle.api.instrumentation" : {
      "subDir" : "src",
      "sourceDirs" : ["src"],
      "dependencies" : ["com.oracle.truffle.api.profiles"],
      "exports" : [
        "<package-info>", # exports all packages containing package-info.java
      ],
      "checkstyle" : "com.oracle.truffle.api",
      "javaCompliance" : "8+",
      "workingSets" : "API,Truffle",
    },

    "com.oracle.truffle.api.instrumentation.test" : {
      "subDir" : "src",
      "sourceDirs" : ["src"],
      "dependencies" : [
        "com.oracle.truffle.api.debug",
        "com.oracle.truffle.api.dsl.test",
        "mx:JUNIT"
      ],
      "checkstyle" : "com.oracle.truffle.api",
      "annotationProcessors" : ["TRUFFLE_DSL_PROCESSOR"],
      "javaCompliance" : "8+",
      "workingSets" : "API,Truffle",
    },

    "com.oracle.truffle.api.debug" : {
      "subDir" : "src",
      "sourceDirs" : ["src"],
      "dependencies" : ["com.oracle.truffle.polyglot"],
      "generatedDependencies" : ["com.oracle.truffle.polyglot"],
      "runtimeDeps" : [
        "java.desktop"
      ],
      "exports" : [
        "<package-info>", # exports all packages containing package-info.java
      ],
      "checkstyle" : "com.oracle.truffle.api",
      "annotationProcessors" : ["TRUFFLE_DSL_PROCESSOR_INTERNAL"],
      "javaCompliance" : "8+",
      "workingSets" : "API,Truffle",
    },

    "com.oracle.truffle.api.debug.test" : {
      "subDir" : "src",
      "sourceDirs" : ["src"],
      "dependencies" : [
        "com.oracle.truffle.api.debug",
        "com.oracle.truffle.api.instrumentation.test",
        "com.oracle.truffle.api.dsl.test",
        "com.oracle.truffle.tck",
        "mx:JUNIT"
      ],
      "checkstyle" : "com.oracle.truffle.api",
      "annotationProcessors" : ["TRUFFLE_DSL_PROCESSOR_INTEROP_INTERNAL"],
      "javaCompliance" : "8+",
      "workingSets" : "API,Truffle",
      "testProject" : True,
    },

    "com.oracle.truffle.api.object" : {
      "subDir" : "src",
      "sourceDirs" : ["src"],
      "dependencies" : [
        "com.oracle.truffle.api.interop",
        "com.oracle.truffle.api.utilities"
      ],
      "exports" : [
        "<package-info>", # exports all packages containing package-info.java
      ],
      "checkstyle" : "com.oracle.truffle.api",
      "javaCompliance" : "8+",
      "workingSets" : "API,Truffle",
    },

    "com.oracle.truffle.api.object.dsl" : {
      "subDir" : "src",
      "sourceDirs" : ["src"],
      "dependencies" : ["com.oracle.truffle.api.object"],
      "exports" : [
        "<package-info>", # exports all packages containing package-info.java
      ],
      "checkstyle" : "com.oracle.truffle.api",
      "javaCompliance" : "8+",
      "workingSets" : "API,Truffle",
    },

    "com.oracle.truffle.api.object.dsl.test" : {
      "subDir" : "src",
      "sourceDirs" : ["src"],
      "dependencies" : [
        "com.oracle.truffle.api.object",
        "com.oracle.truffle.object.basic",
        "com.oracle.truffle.object.dsl.processor",
        "mx:JUNIT",
      ],
      "checkstyle" : "com.oracle.truffle.api",
      "javaCompliance" : "8+",
      "annotationProcessors" : ["TRUFFLE_DSL_PROCESSOR"],
      "workingSets" : "API,Truffle,Codegen,Test",
      "jacoco" : "exclude",
      "testProject" : True,
    },

    "com.oracle.truffle.object.dsl.processor" : {
      "subDir" : "src",
      "sourceDirs" : ["src"],
      "dependencies" : [
        "com.oracle.truffle.api.object.dsl",
        "com.oracle.truffle.dsl.processor"
      ],
      "checkstyle" : "com.oracle.truffle.dsl.processor",
      "javaCompliance" : "8+",
      "workingSets" : "Truffle,Codegen",
    },

    "com.oracle.truffle.api.profiles" : {
      "subDir" : "src",
      "sourceDirs" : ["src"],
      "dependencies" : ["com.oracle.truffle.api"],
      "exports" : [
        "<package-info>", # exports all packages containing package-info.java
      ],
      "checkstyle" : "com.oracle.truffle.api",
      "javaCompliance" : "8+",
      "workingSets" : "API,Truffle",
    },

    "com.oracle.truffle.object" : {
      "subDir" : "src",
      "sourceDirs" : ["src"],
      "dependencies" : ["com.oracle.truffle.api.object"],
      "checkstyle" : "com.oracle.truffle.api",
      "javaCompliance" : "8+",
      "workingSets" : "Truffle",
    },

    "com.oracle.truffle.object.basic" : {
      "subDir" : "src",
      "sourceDirs" : ["src"],
      "dependencies" : ["com.oracle.truffle.object"],
      "checkstyle" : "com.oracle.truffle.api",
      "javaCompliance" : "8+",
      "workingSets" : "Truffle",
    },

    "com.oracle.truffle.object.basic.test" : {
      "subDir" : "src",
      "sourceDirs" : ["src"],
      "dependencies" : [
        "com.oracle.truffle.object.basic",
        "mx:JUNIT"
      ],
      "checkstyle" : "com.oracle.truffle.dsl.processor",
      "javaCompliance" : "8+",
      "workingSets" : "Truffle",
      "testProject" : True,
    },

    "com.oracle.truffle.tck" : {
      "subDir" : "src",
      "sourceDirs" : ["src"],
      "dependencies" : [
        "TRUFFLE_API",
        "mx:JUNIT",
        "sdk:POLYGLOT_TCK"
      ],
      "annotationProcessors" : ["TRUFFLE_DSL_PROCESSOR"],
      "checkstyle" : "com.oracle.truffle.api",
      "javaCompliance" : "8+",
      "workingSets" : "Truffle,Tools",
    },
    "com.oracle.truffle.tck.common" : {
      "subDir" : "src",
      "sourceDirs" : ["src"],
      "dependencies" : [
        "sdk:POLYGLOT_TCK"
      ],
      "checkstyle" : "com.oracle.truffle.api",
      "javaCompliance" : "8+",
      "workingSets" : "Truffle,Tools",
    },
    "com.oracle.truffle.tck.tests" : {
      "subDir" : "src",
      "sourceDirs" : ["src"],
      "dependencies" : [
        "mx:JUNIT",
        "sdk:POLYGLOT_TCK",
        "com.oracle.truffle.tck.common",
      ],
      "uses":[
        "org.graalvm.polyglot.tck.LanguageProvider"
      ],
      "checkstyle" : "com.oracle.truffle.api",
      "javaCompliance" : "8+",
      "workingSets" : "Truffle,Tools",
      "testProject" : True,
    },
    "com.oracle.truffle.tck.instrumentation" : {
      "subDir" : "src",
      "sourceDirs" : ["src"],
      "dependencies" : [
        "mx:JUNIT",
        "TRUFFLE_API",
        "com.oracle.truffle.tck.common",
      ],
      "annotationProcessors" : ["TRUFFLE_DSL_PROCESSOR"],
      "checkstyle" : "com.oracle.truffle.api",
      "javaCompliance" : "8+",
      "workingSets" : "Truffle,Tools",
    },

    "com.oracle.truffle.nfi" : {
      "subDir" : "src",
      "sourceDirs" : ["src"],
      "jniHeaders" : True,
      "dependencies" : [
        "com.oracle.truffle.api.interop",
        "com.oracle.truffle.nfi.types",
      ],
      "exports" : [
        "<package-info>", # exports all packages containing package-info.java
      ],
      "checkstyle" : "com.oracle.truffle.api",
      "javaCompliance" : "8+",
      "annotationProcessors" : ["TRUFFLE_DSL_PROCESSOR_INTEROP_INTERNAL"],
      "workingSets" : "Truffle",
      "os_arch" : {
        "windows" : {
          "<others>" : {
            "ignore" : "windows is not supported",  # necessary until Truffle is fully supported (GR-7941)
          },
        },
        "<others>" : {
          "<others>" : {
            "ignore" : False,
          },
        },
      },
    },

    "com.oracle.truffle.nfi.types" : {
      "subDir" : "src",
      "sourceDirs" : ["src"],
      "dependencies" : [
      ],
      "checkstyle" : "com.oracle.truffle.api",
      "javaCompliance" : "8+",
      "workingSets" : "Truffle",
    },

    "com.oracle.truffle.nfi.native" : {
      "subDir" : "src",
      "native" : True,
      "vpath" : True,
      "results" : [
        "bin/<lib:trufflenfi>",
      ],
      "headers" : [
        "include/trufflenfi.h"
      ],
      "buildDependencies" : [
        "com.oracle.truffle.nfi",
      ],
      "buildEnv" : {
        "CPPFLAGS" : "-I<jnigen:com.oracle.truffle.nfi>",
        "LIBFFI_SRC" : "<path:LIBFFI>",
        "LIBTRUFFLENFI" : "<lib:trufflenfi>",
        "OS" : "<os>",
      },
    },

    "com.oracle.truffle.nfi.test" : {
      "subDir" : "src",
      "sourceDirs" : ["src"],
      "dependencies" : [
        "mx:JUNIT",
        "TRUFFLE_NFI",
        "TRUFFLE_TCK",
        "TRUFFLE_TEST_NATIVE",
      ],
      "checkstyle" : "com.oracle.truffle.api",
      "javaCompliance" : "8+",
      "workingSets" : "Truffle",
      "annotationProcessors" : ["TRUFFLE_DSL_PROCESSOR"],
      "javaProperties" : {
        "native.test.lib" : "<path:TRUFFLE_TEST_NATIVE>/<lib:nativetest>"
      },
      "testProject" : True,
    },

    "com.oracle.truffle.nfi.test.native" : {
      "subDir" : "src",
      "native" : True,
      "vpath" : True,
      "results" : [
        "bin/<lib:nativetest>",
      ],
      "buildDependencies" : [
        "TRUFFLE_NFI_NATIVE",
      ],
      "buildEnv" : {
        "TARGET" : "bin/<lib:nativetest>",
        "CPPFLAGS" : "-I<path:TRUFFLE_NFI_NATIVE>/include",
        "OS" : "<os>",
      },
      "testProject" : True,
    },

    "com.oracle.truffle.sl" : {
      "subDir" : "src",
      "sourceDirs" : ["src"],
      "dependencies" : [
        "TRUFFLE_API",
        "truffle:ANTLR4"
      ],
      "javaCompliance" : "8+",
      "checkstyleVersion" : "8.8",
      "annotationProcessors" : ["TRUFFLE_DSL_PROCESSOR"],
      "workingSets" : "Truffle,SimpleLanguage",
    },

    "com.oracle.truffle.sl.launcher" : {
      "subDir" : "src",
      "sourceDirs" : ["src"],
      "dependencies" : [
        "sdk:GRAAL_SDK",
      ],
      "checkstyle" : "com.oracle.truffle.sl",
      "javaCompliance" : "8+",
      "workingSets" : "Truffle,SimpleLanguage",
    },

    "com.oracle.truffle.sl.test" : {
      "subDir" : "src",
      "sourceDirs" : ["src"],
      "dependencies" : [
        "com.oracle.truffle.tck",
        "com.oracle.truffle.sl",
        "mx:JMH_1_21",
      ],
      "checkstyle" : "com.oracle.truffle.sl",
      "javaCompliance" : "8+",
      "workingSets" : "Truffle,SimpleLanguage,Test",
      "annotationProcessors" : ["TRUFFLE_DSL_PROCESSOR", "mx:JMH_1_21"],
      "testProject" : True,
    },
   },

  "licenses" : {
    "UPL" : {
      "name" : "Universal Permissive License, Version 1.0",
      "url" : "http://opensource.org/licenses/UPL",
    }
  },

  "distributions" : {

    # ------------- Distributions -------------

    "TRUFFLE_API" : {
      # This distribution defines a module.
      "moduleName" : "org.graalvm.truffle",
      "subDir" : "src",
      "javaCompliance" : "8+",
      "dependencies" : [
        "com.oracle.truffle.api.dsl",
        "com.oracle.truffle.api.profiles",
        "com.oracle.truffle.api.debug",
        "com.oracle.truffle.api.utilities",
        "com.oracle.truffle.object.basic",
        "com.oracle.truffle.api.object.dsl",
        "com.oracle.truffle.polyglot",
      ],
      "distDependencies" : [
        "sdk:GRAAL_SDK"
      ],
      "description" : "Truffle is a multi-language framework for executing dynamic languages\nthat achieves high performance when combined with Graal.",
      "javadocType": "api",
    },

    "TRUFFLE_NFI" : {
      # This distribution defines a module.
      "moduleName" : "com.oracle.truffle.truffle_nfi",
      "subDir" : "src",
      "javaCompliance" : "8+",
      "dependencies" : [
        "com.oracle.truffle.nfi",
      ],
      "distDependencies" : [
        "TRUFFLE_API",
        "TRUFFLE_NFI_NATIVE",
      ],
      "javaProperties" : {
          "truffle.nfi.library" : "<path:TRUFFLE_NFI_NATIVE>/bin/<lib:trufflenfi>"
      },
      "description" : """Native function interface for the Truffle framework.""",
      "allowsJavadocWarnings": True,
    },

    "TRUFFLE_NFI_NATIVE" : {
      "native" : True,
      "relpath" : True,
      "platformDependent" : True,
      "platforms" : [
          "linux-amd64",
          "darwin-amd64",
      ],
      "output" : "<mxbuild>/truffle-nfi-native",
      "dependencies" : [
        "com.oracle.truffle.nfi.native",
      ],
      "description" : """Contains the native library needed by truffle-nfi.""",
      "maven": True,
    },

    "TRUFFLE_TCK" : {
      "subDir" : "src",
      "javaCompliance" : "8+",
      "dependencies" : [
        "com.oracle.truffle.tck"
      ],
      "distDependencies" : [
        "TRUFFLE_API",
        "sdk:POLYGLOT_TCK",
      ],
      "exclude" : ["mx:JUNIT"],
      "description" : "A collection of tests that can certify language implementation to be compliant\nwith most recent requirements of the Truffle infrastructure and tooling.",
      "allowsJavadocWarnings": True,
    },

    "TRUFFLE_TCK_COMMON" : {
      "subDir" : "src",
      "javaCompliance" : "8+",
      "dependencies" : [
        "com.oracle.truffle.tck.common"
      ],
      "distDependencies" : [
        "sdk:POLYGLOT_TCK",
      ],
      "description" : "Common types for TCK Tests and Instruments.",
      "allowsJavadocWarnings": True,
    },

    "TRUFFLE_TCK_TESTS" : {
      "subDir" : "src",
      "javaCompliance" : "8+",
      "dependencies" : [
        "com.oracle.truffle.tck.tests"
      ],
      "distDependencies" : [
        "sdk:POLYGLOT_TCK",
        "TRUFFLE_TCK_COMMON"
      ],
      "exclude" : ["mx:JUNIT"],
      "description" : "A collection of tests that can certify language implementation to be compliant\nwith most recent requirements of the Truffle infrastructure and tooling.",
      "allowsJavadocWarnings": True,
      "testProject" : True,
    },

    "TRUFFLE_TCK_INSTRUMENTATION" : {
      "subDir" : "src",
      "javaCompliance" : "8+",
      "dependencies" : [
        "com.oracle.truffle.tck.instrumentation"
      ],
      "distDependencies" : [
        "TRUFFLE_API",
        "TRUFFLE_TCK_COMMON"
      ],
      "exclude" : ["mx:JUNIT"],
      "description" : "Instruments used by the Truffle TCK.",
      "allowsJavadocWarnings": True,
    },

    "TRUFFLE_DSL_PROCESSOR_INTERNAL" : {
      "internal" : True,
      "subDir" : "src",
      "dependencies" : ["com.oracle.truffle.dsl.processor", "com.oracle.truffle.dsl.processor.jdk9"],
      "distDependencies" : ["sdk:GRAAL_SDK"],
      "maven" : False,
    },

    "TRUFFLE_DSL_PROCESSOR_INTEROP_INTERNAL" : {
      "internal" : True,
      "subDir" : "src",
      "dependencies" : ["com.oracle.truffle.dsl.processor", "com.oracle.truffle.dsl.processor.interop", "com.oracle.truffle.dsl.processor.jdk9"],
      "distDependencies" : ["sdk:GRAAL_SDK"],
      "maven" : False,
    },

    "TRUFFLE_DSL_PROCESSOR" : {
      "subDir" : "src",
      "dependencies" : ["com.oracle.truffle.dsl.processor", "com.oracle.truffle.dsl.processor.interop", "com.oracle.truffle.object.dsl.processor", "com.oracle.truffle.dsl.processor.jdk9", "truffle:ANTLR4"],
      "distDependencies" : ["TRUFFLE_API"],
      "description" : "The Truffle DSL Processor generates source code for nodes that are declared using the DSL.",
      "allowsJavadocWarnings": True,
    },

    "TRUFFLE_SL" : {
      "subDir" : "src",
      "javaCompliance" : "8+",
      "dependencies" : [
        "com.oracle.truffle.sl",
      ],
      "exclude" : [
        "mx:JUNIT",
        "truffle:ANTLR4",
      ],
      "distDependencies" : [
          "TRUFFLE_API",
          "TRUFFLE_TCK",
      ],
      "description" : "Truffle SL is an example language implemented using the Truffle API.",
      "allowsJavadocWarnings": True,
    },

    "TRUFFLE_SL_LAUNCHER" : {
      "subDir" : "src",
      "javaCompliance" : "8+",
      "dependencies" : [
        "com.oracle.truffle.sl.launcher",
      ],
      "distDependencies" : [
          "sdk:GRAAL_SDK",
      ],
      "description" : "Truffle SL launchers using the polyglot API.",
      "allowsJavadocWarnings": True,
    },

    "TRUFFLE_SL_TEST" : {
      "subDir" : "src",
      "javaCompliance" : "8+",
      "dependencies" : [
        "com.oracle.truffle.sl.test"
      ],
      "exclude" : [
        "mx:JUNIT",
        "mx:JMH_1_21"
      ],
      "distDependencies" : [
          "TRUFFLE_API",
          "TRUFFLE_TCK",
          "TRUFFLE_SL"
      ],
      "maven" : False
    },

    "TRUFFLE_SL_TCK" : {
      "subDir" : "src",
      "javaCompliance" : "8+",
      "dependencies" : [
        "com.oracle.truffle.sl.tck"
      ],
      "exclude" : [
        "mx:JUNIT",
      ],
      "distDependencies" : [
        "sdk:POLYGLOT_TCK"
      ],
      "maven" : False
    },

    "TRUFFLE_INSTRUMENT_TEST" : {
      "subDir" : "src",
      "javaCompliance" : "8+",
      "dependencies" : [
        "com.oracle.truffle.api.instrumentation.test",
      ],
      "exclude" : ["mx:HAMCREST", "mx:JUNIT", "mx:JMH_1_21"],
      "distDependencies" : [
        "TRUFFLE_API",
        "TRUFFLE_DSL_PROCESSOR",
      ],
      "description" : "Instrumentation tests including InstrumentationTestLanguage.",
      "allowsJavadocWarnings": True,
    },

     "TRUFFLE_TEST" : {
       "subDir" : "src",
       "javaCompliance" : "8+",
       "dependencies" : [
         "com.oracle.truffle.api.test",
         "com.oracle.truffle.api.benchmark",
         "com.oracle.truffle.api.dsl.test",
         "com.oracle.truffle.api.instrumentation.test",
         "com.oracle.truffle.api.debug.test",
         "com.oracle.truffle.api.object.dsl.test",
         "com.oracle.truffle.object.basic.test",
         "com.oracle.truffle.nfi.test",
       ],
       "exclude" : ["mx:HAMCREST", "mx:JUNIT", "mx:JMH_1_21"],
       "distDependencies" : [
         "TRUFFLE_API",
         "TRUFFLE_NFI",
         "TRUFFLE_DSL_PROCESSOR",
         "TRUFFLE_INSTRUMENT_TEST",
         "TRUFFLE_TEST_NATIVE",
         "TRUFFLE_TCK",
      ],
      "maven" : False,
     },

     "TRUFFLE_TEST_NATIVE" : {
       "native" : True,
       "platformDependent" : True,
       "output" : "<mxbuild>/truffle-test-native",
       "dependencies" : [
         "com.oracle.truffle.nfi.test.native",
       ],
       "testDistribution" : True,
      "maven" : False,
     },

    "TRUFFLE_GRAALVM_SUPPORT" : {
      "native" : True,
      "description" : "Truffle support distribution for the GraalVM",
      "layout" : {
        "native-image.properties" : "file:mx.truffle/tools-truffle.properties",
        "builder/" : "dependency:truffle:TRUFFLE_NFI",
      },
    },
  },
}
