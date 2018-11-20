//
//  Use this file to import your target's public headers that you would like to expose to Swift.
//

#define uECC_WORD_SIZE 1
#import <stdio.h>
#import "uECC.h"

void vli_print(uint8_t *vli, unsigned int size) {
    for(unsigned i=0; i<size; ++i) {
        printf("%02X ", (unsigned)vli[i]);
    }
}

static
void checkKeys() {
#define PRIVATE_SIZE 21
#define PUBLIC_SIZE 40
#define SECRET_SIZE 20
    
    uint8_t private1[PRIVATE_SIZE] = {0};
    uint8_t private2[PRIVATE_SIZE] = {0};
    uint8_t public1[PUBLIC_SIZE] = {0};
    uint8_t public2[PUBLIC_SIZE] = {0};
    uint8_t secret1[SECRET_SIZE] = {0};
    uint8_t secret2[SECRET_SIZE] = {0};
    
    uECC_Curve curve = uECC_secp160r1();
    
    printf("Testing random private key pairs\n");
    
    uECC_make_key(public1, private1, curve);
    uECC_make_key(public2, private2, curve);
    
    
    uECC_shared_secret(public2, private1, secret1, curve);
    uECC_shared_secret(public1, private2, secret2, curve);
    
    printf("Private key 1 = ");
    vli_print(private1, PRIVATE_SIZE);
    printf("\n");
    printf("Private key 2 = ");
    vli_print(private2, PRIVATE_SIZE);
    printf("\n");
    printf("Public key 1 = ");
    vli_print(public1, PUBLIC_SIZE);
    printf("\n");
    printf("Public key 2 = ");
    vli_print(public2, PUBLIC_SIZE);
    printf("\n");
    printf("Shared secret 1 = ");
    vli_print(secret1, SECRET_SIZE);
    printf("\n");
    printf("Shared secret 2 = ");
    vli_print(secret2, SECRET_SIZE);
    printf("\n");
}
