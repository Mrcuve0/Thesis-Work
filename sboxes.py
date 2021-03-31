sbox = [
    # 0     1     2     3     4     5     6     7     8     9     a     b     c     d     e     f
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76, # 0
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0, # 1
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15, # 2
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75, # 3
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84, # 4
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf, # 5
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8, # 6
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2, # 7
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73, # 8
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb, # 9
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79, # a
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08, # b
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a, # c
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e, # d
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf, # e
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16  # f
]

sbox_freyre_1 = [
    # 0     1     2     3     4     5     6     7     8     9     a     b     c     d     e     f
    0xF2, 0x35, 0x3C, 0xA6, 0xE5, 0xC0, 0x8C, 0xBF, 0x0D, 0xA7, 0xEC, 0x08, 0xE4, 0x8B, 0x79, 0x59, # 0
    0x85, 0x3A, 0xCA, 0x55, 0xDE, 0x07, 0x20, 0xFA, 0x11, 0x3E, 0xFF, 0x19, 0xE8, 0xDC, 0x1E, 0xC9, # 1
    0x91, 0xA5, 0x47, 0x4B, 0x43, 0xDB, 0xC7, 0x12, 0xBD, 0x90, 0xA2, 0xBE, 0x9E, 0x93, 0xF8, 0xA1, # 2
    0xC6, 0x6C, 0x1D, 0xB8, 0xA0, 0x7C, 0xFB, 0x4C, 0xD7, 0x86, 0x80, 0xF9, 0x8A, 0x2D, 0xB6, 0x96, # 3
    0x95, 0x9B, 0x17, 0xE2, 0x6B, 0x40, 0x89, 0xED, 0xD0, 0xDD, 0x57, 0x00, 0xE0, 0xA3, 0xBB, 0xF4, # 4
    0xA4, 0x70, 0x63, 0xF1, 0x7D, 0x48, 0x44, 0x6F, 0x0E, 0xAF, 0x3D, 0x03, 0xB5, 0xA9, 0x13, 0xD5, # 5
    0xA8, 0x94, 0x78, 0xAA, 0x18, 0x9F, 0x97, 0x22, 0x7E, 0x81, 0x26, 0xFC, 0xB9, 0x5E, 0x83, 0x62, # 6
    0x33, 0x9C, 0x2A, 0xEA, 0x50, 0xCD, 0xEE, 0x05, 0xFE, 0x30, 0x04, 0xD3, 0x0B, 0xC3, 0x87, 0x5C, # 7
    0x74, 0x1C, 0x7A, 0x71, 0x5F, 0x29, 0x28, 0x1F, 0x61, 0xDA, 0xDF, 0x46, 0x4E, 0x6D, 0xB1, 0x2E, # 8
    0x6A, 0x5D, 0x65, 0x5A, 0xD6, 0x88, 0x34, 0xF3, 0x32, 0xF6, 0x73, 0x58, 0x69, 0xC2, 0x66, 0xD8, # 9
    0x39, 0xD2, 0x4A, 0x99, 0x06, 0x6E, 0x3F, 0xC4, 0xE7, 0x2C, 0x49, 0x3B, 0xC8, 0xD4, 0xF0, 0xD9, # A
    0xD1, 0x4D, 0xB2, 0x0F, 0x92, 0xB7, 0xAE, 0x84, 0x37, 0x14, 0x21, 0x7F, 0x8F, 0x56, 0x8E, 0x98, # B
    0x1A, 0x68, 0x67, 0xE9, 0x9D, 0x25, 0x09, 0xCB, 0x41, 0xAD, 0xCF, 0x51, 0x72, 0xE3, 0x64, 0x16, # C
    0xCC, 0xBA, 0xC5, 0xB4, 0x5B, 0x01, 0x52, 0xF5, 0xC1, 0xFD, 0x77, 0x02, 0xB0, 0x38, 0x27, 0x8D, # D
    0xE6, 0x36, 0xAC, 0x45, 0x0C, 0x75, 0x7B, 0x82, 0xEB, 0x24, 0x42, 0xBC, 0x31, 0x60, 0x9A, 0x76, # E
    0x2B, 0x1B, 0x4F, 0x2F, 0x23, 0xEF, 0xCE, 0x10, 0xB3, 0x0A, 0x54, 0xF7, 0xE1, 0xAB, 0x15, 0x53  # F
]

sbox_freyre_2 = [
    # 0     1     2     3     4     5     6     7     8     9     a     b     c     d     e     f
    0x55, 0x38, 0x84, 0x9B, 0x5C, 0x3D, 0xC0, 0xF6, 0xF2, 0x02, 0xC3, 0x4C, 0xBF, 0xC4, 0xE9, 0xC7, # 0
    0x34, 0x94, 0x9D, 0x8C, 0xCE, 0xAE, 0xED, 0x86, 0x50, 0x67, 0x69, 0x4A, 0x90, 0xBB, 0xD2, 0xB4, # 1
    0x11, 0xAF, 0xF0, 0xE8, 0x5A, 0xFD, 0xB9, 0x47, 0xB1, 0x95, 0xD9, 0x40, 0x4B, 0x27, 0xBE, 0x54, # 2
    0x9E, 0x14, 0x07, 0x65, 0x7D, 0x89, 0x3E, 0x63, 0xA9, 0x1D, 0x82, 0x2F, 0x1F, 0x78, 0x2A, 0x7E, # 3
    0xC2, 0xC5, 0x01, 0x6F, 0xB5, 0xDA, 0x60, 0xEB, 0xE7, 0xA4, 0x0F, 0x1C, 0xDF, 0x19, 0x74, 0x72, # 4
    0x62, 0x44, 0x6E, 0x80, 0x73, 0x6C, 0xF9, 0xC8, 0x48, 0xB6, 0x33, 0x2B, 0x68, 0xFC, 0x8E, 0x37, # 5
    0x10, 0x3B, 0xA6, 0x96, 0xC1, 0xCF, 0x57, 0xEA, 0x8A, 0x6A, 0xE3, 0x08, 0x8D, 0xB2, 0xBD, 0x52, # 6
    0x7A, 0x88, 0xB0, 0x1B, 0xD7, 0x2C, 0xE6, 0x66, 0x91, 0x9A, 0x06, 0x6B, 0x59, 0x17, 0x83, 0xDB, # 7
    0xD5, 0x22, 0x85, 0x4D, 0xFE, 0x0B, 0xAD, 0xF4, 0x56, 0x32, 0x03, 0x5E, 0xB3, 0xDC, 0x26, 0x7B, # 8
    0x16, 0xCD, 0x4E, 0x2E, 0x21, 0xFF, 0xAC, 0x79, 0xA1, 0x23, 0xEC, 0x04, 0xC6, 0xE4, 0x7F, 0x28, # 9
    0x53, 0x39, 0xCB, 0xA0, 0xD4, 0x7C, 0xFB, 0x3A, 0x0C, 0x5D, 0x58, 0x92, 0x05, 0x3F, 0xD6, 0x5B, # A
    0x25, 0x61, 0x12, 0xBC, 0xA3, 0xE1, 0x29, 0x5F, 0x75, 0x41, 0x1A, 0x98, 0xDE, 0x51, 0x4F, 0x93, # B
    0x97, 0x24, 0xE2, 0x49, 0xB7, 0xE0, 0x36, 0x8B, 0xB8, 0xD8, 0x18, 0xF1, 0xC9, 0xE5, 0x31, 0xF5, # C
    0x30, 0xA7, 0x43, 0x0E, 0xA8, 0xF7, 0x6D, 0x8F, 0xCC, 0x99, 0xEE, 0x42, 0xD3, 0x1E, 0xF8, 0x45, # D
    0x2D, 0xA2, 0xDD, 0x20, 0x9C, 0xAA, 0xEF, 0x81, 0x64, 0x77, 0x46, 0x0D, 0x13, 0x76, 0x35, 0xD1, # E
    0xD0, 0x71, 0x00, 0xF3, 0x87, 0xA5, 0x15, 0x9F, 0xAB, 0x0A, 0x70, 0xCA, 0xFA, 0x09, 0x3C, 0xBA  # F
]

sbox_freyre_3 = [
    # 0     1     2     3     4     5     6     7     8     9     a     b     c     d     e     f
    0xCC, 0x35, 0x88, 0x65, 0x05, 0xC1, 0x0D, 0x91, 0x99, 0x61, 0x4B, 0xF8, 0xFB, 0xEC, 0x77, 0xFA, # 0
    0x28, 0x92, 0x02, 0x89, 0x13, 0xB0, 0x3B, 0x39, 0x3A, 0x95, 0xB9, 0x33, 0xB8, 0x94, 0xB5, 0xDA, # 1
    0xC7, 0xBF, 0x7A, 0x6F, 0x87, 0x54, 0x34, 0xF6, 0x66, 0x48, 0x10, 0xAA, 0x29, 0x9D, 0x98, 0xD9, # 2
    0x76, 0xA8, 0x17, 0x09, 0x3F, 0x27, 0xD5, 0x57, 0x3E, 0x24, 0x6C, 0x3C, 0x49, 0x14, 0x8E, 0x42, # 3
    0x1B, 0x18, 0x43, 0x6A, 0x5B, 0x93, 0xC8, 0x90, 0xFF, 0xFC, 0xF3, 0xE6, 0xA9, 0x8A, 0xF9, 0x2E, # 4
    0x4A, 0xAE, 0x59, 0x96, 0x44, 0xC5, 0x04, 0x51, 0x2C, 0x4E, 0x9C, 0xF2, 0x1F, 0x4F, 0xBB, 0x9B, # 5
    0x23, 0x2D, 0xD3, 0xC6, 0xCF, 0xCA, 0xAD, 0xCB, 0xE0, 0xA6, 0xFE, 0x31, 0x74, 0xB3, 0x45, 0x46, # 6
    0xB6, 0x7D, 0xEE, 0x1E, 0xEB, 0x6B, 0xEA, 0x7F, 0x1C, 0x01, 0xF0, 0x08, 0x4C, 0x1A, 0x6D, 0x2F, # 7
    0x38, 0x85, 0x82, 0x06, 0xE4, 0xD4, 0x75, 0x69, 0x7E, 0x8F, 0xB1, 0x9F, 0xB2, 0x5D, 0xBA, 0x41, # 8
    0x56, 0x63, 0x8C, 0x9A, 0x62, 0x0E, 0xC2, 0x80, 0x36, 0x78, 0x0F, 0x1D, 0x4D, 0xFD, 0xDE, 0xE7, # 9
    0xA3, 0x73, 0xAC, 0xAF, 0xD2, 0x2B, 0x67, 0xF7, 0x0B, 0xD7, 0x8D, 0xA7, 0x12, 0x22, 0x0C, 0x53, # A
    0xF4, 0x8B, 0x5A, 0xCD, 0x79, 0xAB, 0x52, 0x19, 0x20, 0x2A, 0x81, 0x84, 0xE8, 0xDC, 0x16, 0xE3, # B
    0x32, 0xE1, 0x68, 0x37, 0xD0, 0xA4, 0x58, 0x72, 0x6E, 0x71, 0xA5, 0xC3, 0xED, 0x5F, 0x7B, 0xDB, # C
    0x00, 0x11, 0x03, 0x50, 0x40, 0x21, 0x25, 0x30, 0xE9, 0x5E, 0xF1, 0xB7, 0xE5, 0xB4, 0x70, 0x55, # D
    0xDF, 0x3D, 0xD6, 0x9E, 0x47, 0x5C, 0xC4, 0x97, 0x86, 0xCE, 0x60, 0xC0, 0x15, 0x26, 0xD1, 0xD8, # E
    0x7C, 0xBE, 0xA2, 0x64, 0xBC, 0xEF, 0xDD, 0xF5, 0xBD, 0x0A, 0xA1, 0xE2, 0xA0, 0xC9, 0x83, 0x07  # F
]