try:
    from Crypto.PublicKey import RSA
    from Crypto.Random import get_random_bytes
    from Crypto.Cipher import AES
    import argparse
    import json
except ImportError:
    print("Please run 'pip install -r requirements.txt'")
    exit(1)

def decrypt_aes(fp, key):
    nonce, tag, ciphertext = [fp.read(i) for i in (16, 16, -1)]
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)

def main():
    parser = argparse.ArgumentParser(description='Unpack Keystore')
    parser.add_argument('output_pks', help='Output private key store directory')
    args = parser.parse_args()

    master_key = input("Enter master key hex: ")
    try:
        master_key = bytes.fromhex(master_key)
    except ValueError:
        print("Invalid hex string")
        return
    
    print("Reading metadata file...")
    with open(f'metadata.json', 'rb') as f:
        metadata = decrypt_aes(f, master_key)
        metadata = metadata.decode()
        metadata = json.loads(metadata)

    print("Reading private RSA keys...")
    for i in range(metadata['num_keys_rsa']):
        with open(f'private_key_{i}.pem_crypt', 'rb') as f:
            private_key = decrypt_aes(f, master_key)
            with open(f'{args.output_pks}/private_key_{i}.pem', 'wb') as f:
                f.write(private_key)
    
    print("Reading private AES keys...")
    for i in range(metadata['num_keys_aes']):
        with open(f'aes_key_{i}.crypt', 'rb') as f:
            key = decrypt_aes(f, master_key)
            with open(f'{args.output_pks}/aes_key_{i}.key', 'wb') as f:
                f.write(key)
    
    print("Done")

if __name__ == '__main__':
    main()