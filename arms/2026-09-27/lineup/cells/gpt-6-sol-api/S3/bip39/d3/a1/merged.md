# BIP: 39

## Abstract
This BIP describes a mnemonic code, or mnemonic sentence—a sequence of easy-to-remember words—for generating deterministic wallets. It has two parts: generating a mnemonic and converting it into a binary seed. The seed can then be used to generate deterministic wallets using BIP-0032 or similar methods.

## Copyright
This BIP is licensed under the MIT license.

## Motivation
A mnemonic sentence is easier for people to use than a wallet seed in raw binary or hexadecimal form. The sentence could be written on paper or spoken over the telephone.

The method provides a human-readable transcription for transporting computer-generated determinism. It is not intended to turn user-created sentences (brainwallets) into a wallet seed.

## Generating the mnemonic
The mnemonic encodes entropy whose length is a multiple of 32 bits. Greater entropy improves security but lengthens the sentence. ENT denotes the initial entropy length. The allowed values of ENT are 128, 160, 192, 224, and 256 bits.

First, generate ENT bits of initial entropy. Take the first ENT / 32 bits of the SHA-256 hash of that entropy as the checksum. Append the checksum to the end of the initial entropy. Split the resulting bit sequence into groups of 11 bits, each representing a number from 0-2047 that indexes a wordlist. Convert the indices to words and join the words into a mnemonic sentence.

The following table describes the relation between the initial entropy length (ENT), the checksum length (CS), and the length of the generated mnemonic sentence (MS) in words.

```
 CS = ENT / 32
 MS = (ENT + CS) / 11
 
 |  ENT  | CS | ENT+CS |  MS  |
 +-------+----+--------+------+
 |  128  |  4 |   132  |  12  |
 |  160  |  5 |   165  |  15  |
 |  192  |  6 |   198  |  18  |
 |  224  |  7 |   231  |  21  |
 |  256  |  8 |   264  |  24  |
 ```

Source: https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki