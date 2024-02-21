# CryptoPack Usage Manual

## Project Description
CryptoPack is a Python library that allows you to generate and encrypt RSA and AES keys for storage and later decryption with AES 256.

## Usage

```bash
git clone https://github.com/woo200/key_pack.git
cd key_pack
pip install -r requirements.txt
```

Creating a keystore
```bash
python3 key_pack.py output_dir
```

### Options

CryptoPack's `key_pack.py` script supports several command-line options to customize the generation of RSA and AES keys. Here's how you can use them:

- `--key_size`: Specifies the key size in bits for the RSA keys. The default value is 4096 bits. A larger key size means more security but may increase the time it takes to generate and use the keys.
  
  Example: `python3 key_pack.py output_dir --key_size 2048`

- `--num_keys_aes`: Determines the number of AES keys to generate. AES keys are used for symmetric encryption. The default value is 1.
  
  Example: `python3 key_pack.py output_dir --num_keys_aes 5`

- `--num_keys_rsa`: Sets the number of RSA key pairs (public and private) to generate. RSA keys are used for asymmetric encryption and signing. The default value is 1.
  
  Example: `python3 key_pack.py output_dir --num_keys_rsa 2`

- `output_pks`: The directory where the private keys (both RSA and AES) will be stored. This argument is mandatory and specifies the output directory for the private key store. (Usually a flash drive)
  
  Usage is implicit in the command example: `python3 key_pack.py output_dir`

- `--outout_pub_ks`: Specifies the directory where the public keys will be stored. The default directory is named `trusted_keys`. 
  
  Example: `python3 key_pack.py output_dir --outout_pub_ks public_keys`
