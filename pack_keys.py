from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
import argparse
import shutil
import json
import os

def generate_aes_crypt(data, key):
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return cipher.nonce + tag + ciphertext

def main():
    parser = argparse.ArgumentParser(description='Generate RSA key pair')
    parser.add_argument('--key_size', type=int, help='Key size in bits', default=4096)
    parser.add_argument('--num_keys_aes', type=int, help='Number of AES keys to generate', default=1)
    parser.add_argument('--num_keys_rsa', type=int, help='Number of RSA keys to generate', default=1)
    parser.add_argument('output_pks', help='Output private key store directory')
    parser.add_argument('--outout_pub_ks', help='Output public key store directory', default='trusted_keys')
    args = parser.parse_args()

    print("Generating master key...")
    master_key = get_random_bytes(32)

    print("Generating folders...")
    os.makedirs(args.output_pks, exist_ok=True)
    os.makedirs(args.outout_pub_ks, exist_ok=True)

    print("Generating private keys...")
    for i in range(args.num_keys_rsa):
        key = RSA.generate(args.key_size) # Generate a key pair
        private_key = key.export_key()
        public_key = key.publickey().export_key()

        print(f"Encrypting private key {i}...")
        # Encrypt the private key with the master key
        private_key_crypt = generate_aes_crypt(private_key, master_key)

        print(f"Writing keys ({i})...")
        with open(f'{args.output_pks}/private_key_{i}.pem_crypt', 'wb') as f:
            f.write(private_key_crypt)
        with open(f'{args.outout_pub_ks}/public_key_{i}.pem', 'wb') as f:
            f.write(public_key)
    
    print("Generating AES keys...")
    for i in range(args.num_keys_aes):
        key = get_random_bytes(32)
        print(f"Encrypting AES key {i}...")
        # Encrypt the AES key with the master key
        key_crypt = generate_aes_crypt(key, master_key)

        print(f"Writing keys ({i})...")
        with open(f'{args.output_pks}/aes_key_{i}.crypt', 'wb') as f:
            f.write(key_crypt)

    print("Writing metadata file...")
    metadata = {
        "key_size": args.key_size,
        "num_keys_aes": args.num_keys_aes,
        "num_keys_rsa": args.num_keys_rsa,
    }
    with open(f'{args.output_pks}/metadata.json', 'wb') as f:
        json_str = json.dumps(metadata, indent=4)
        e_json_str = generate_aes_crypt(json_str.encode(), master_key)
        f.write(e_json_str)
    
    print("Writing unpack utility...")
    shutil.copyfile('unpack.py', f'{args.output_pks}/unpack.py')
    shutil.copyfile('requirements.txt', f'{args.output_pks}/requirements.txt')

    f_pk = ' '.join(f"{i:02x}" for i in master_key)
    print(f"Private key: \"{f_pk}\"")

if __name__ == '__main__':
    main()