//
//  api.hpp
//  KMP
//
//  Created by Wang Yi on 16/3/17.
//  Copyright © 2017 Wang yiak.co. All rights reserved.
//

#ifndef api_hpp
#define api_hpp

#include <stdio.h>

#define NOT_FOUND -1

#define Malloc(type, len) \
(type*) malloc(sizeof(type)*len)

#define FOR(i, s) \
    for(i=0; i < s; i++) {
#define END ;}

#endif /* api_hpp */
