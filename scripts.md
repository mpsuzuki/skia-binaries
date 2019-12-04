# scripts in this directory

After downloading & updating the source of skia,
you should execute "gn" to generate Ninja input files.

Some options are explained in (their document)[https://skia.org/user/build]
but too few examples for Win32 or Win64 builders.

## how to use

 # Download depot_tools and setup Python2 (almost same with (their document)[https://skia.org/user/build])

```
git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git
export PATH=`pwd`/depot_tools:${PATH}
cd depot_tools
ln -s `which python2.7` python2
ln -s python2 python
cd ..
```

 # Download and synchronize the skia and related components.

```
git clone https://skia.googlesource.com/skia.git
cd skia
python tools/git-sync-deps
```

 # Invoke "gn" for an archive library and fix WSL-syntax pathnames in Ninja files

```
sh -x /somewhere/you/downloaded/scripts/build-skia-static.sh
sh -x /somewhere/you/downloaded/scripts/RewriteWSLPath.sh out/Static
```

 # Invoke "gn" for DLL and fix WSL-syntax pathnames in Ninja files

```
sh -x /somewhere/you/downloaded/scripts/build-skia-shared.sh
sh -x /somewhere/you/downloaded/scripts/RewriteWSLPath.sh out/Shared
```

 # Execute Ninja

```
ninja -v -C out/Static 2>&1 | tee out/Static/LOG.build
ninja -v -C out/Shared 2>&1 | tee out/Shared/LOG.build
```

## what the scripts are doing?

* build-skia-static.sh

This is the most basic 1-line script to invoke "gn" to
build an archive library of Skia, under the environment
described in (README.md)[README.md].

* build-skia-shared.sh

Same with build-skia-static.sh, but do for DLL.
"is_component_build=true" and --shared_library=true are
added.

* RewriteWSLPath.sh

If we execute "gn" under WSL, the generated Ninja files
have WSL-syntax path (MinGW like), as, "/mnt/c/ProgramFiles/...".
Considering that MSVC-compatible interface of clang-cl.exe
accepts DOS-like-syntax path (C:/ProgramFiles/...), it should
be better to rewrite WSL-syntax to DOS-like-syntax.

However, if the Ninja to be executed is a Linux executable on
WSL, it does not accept DOS-like-syntax for the command to
be executed. It should be left in WSL-syntax.
