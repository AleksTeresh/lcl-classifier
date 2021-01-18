# tplClassifier

## Getting started

1. Install round eliminator locally

```
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
git clone -b arbitrary2 https://github.com/olidennis/round-eliminator.git
cd round-eliminator
RUSTFLAGS="-C target-cpu=native" cargo build --release
cd ..
mv round-eliminator/target/release/server 'path-to-tlpClassifier'
```

2. Generating the data set

```
python3 generator.py -w 3 -b 2
```

3. Running the classifier

```
python3 classifier.py -w 3 -b 2
```
