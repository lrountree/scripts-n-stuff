# Search ASM in a given account for a specific value
# Maintained By: Lucas Rountree (lredvtree@gmail.com)

# Import General Modules
import sys

# Import Custom Modules
sys.path.append('../../modules/aws')
from auth_modules import set_session as session
from other_modules import asm

def search_value(PROFILE, REGION, VALUE):
    ses = session(PROFILE, REGION)
    secrets = asm(ses)

    response = []
    secrets_list = secrets.list_secrets()
    if not secrets_list[0]:
        return 'Generating list of secrets failed with: ' + secrets_list[1]
    for SECRET in secrets_list[1]:
        key_list = secrets.secret_keys(SECRET)
        if not key_list[0]:
            print('Secret: ' + SECRET + ' had the following error: ' + key_list[1])
            continue
        for KEY in key_list[1]:
            k_val = secrets.secret_value(SECRET, KEY)
            if not k_val[0]:
                print('Grabbing value of: ' + KEY + ' from: ' + SECRET + ' failed with: ' + k_val[1])
                continue
            if k_val[1] == VALUE:
                response.append('Secret: ' + SECRET + ', Key: ' + KEY + ', Value: ' + k_val[1])
    if not response:
        return False, 'Value Not Found'
    return True, response


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Search ASM', prog='search_asm')
    parser.add_argument('-p', action='store', type=str, default='default', help='AWS profile to use, from credentials/config file.')
    parser.add_argument('-r', action='store', type=str, help='Region specification')
    parser.add_argument('-v', action='store', type=str, help='Secret value to search for')
   
    args = parser.parse_args()

    if args.p is False or args.r is False or args.v is False:
        parser.error('Profile (-p), Region (-r), and Value (-v) are REQUIRED')

    else:
        print(search_value(args.p, args.r, args.v))
