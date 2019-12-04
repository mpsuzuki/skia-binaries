#!/bin/sh

dir=`echo $1 | sed 's:/$::'`
if test -d "$dir".orig
then
  echo reuse existing backup at "$dir".orig
else
  echo backup ninja files in $dir to "$dir".orig
  cp -pr $dir "$dir".orig
fi

for n in `cd $dir && find . -name "*.ninja"`
do
  if test `basename $n` = toolchain.ninja
  then
    echo Append more cflags to "$dir"/$n
    sed 's|command.*/bin/clang-cl.*|& -Wno-unused-result -Wno-shadow-field -Wno-extra-semi-stmt|' < "$dir".orig/$n > "$dir"/$n
  else
    echo Fix "$dir"/$n
    sed "s|/mnt/c/|C:/|g" < "$dir".orig/$n > "$dir"/$n
  fi
done
