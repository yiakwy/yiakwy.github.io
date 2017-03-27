//
//  boyerMoore.cpp
//  boyerMoore
//
//  Created by Wang Yi on 30/10/16.
//  Copyright (c) 2016 Wang Yi. All rights reserved.
//

#include "boyerMoore.h"

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdarg.h>
#include <time.h>

#define ALPHABET_LEN 256
#define NOT_FOUND -1

// operator
#define MAX(self, other) ((self < other) ? other : self)
#define MIN(self, other) ((self < other) ? self : other)

// memory management
#define Malloc(type, len) \
(type*) malloc(sizeof(type) * len)

// for debug purpose
#define __SHORT_FILE__ (strrchr(__FILE__, '/') ? strrchr(__FILE__, '/') + 1 : __FILE__)
#define _FORMATTED_TIME getFormattedTime()
#define _PRE _FORMATTED_TIME

#define windows_width 95
static int _fmt_pos;
// http://stackoverflow.com/questions/1644868/c-define-macro-for-debug-printing
// https://gcc.gnu.org/onlinedocs/gcc/Variadic-Macros.html
// if you use '##' past operator, the compiler will stop to complain about the above statement
#define PRINTER_logger(fmt, ...) \
do { \
fprintf(stderr, "[%s] Info: " fmt "%n", _PRE, ## __VA_ARGS__, &_fmt_pos); \
fprintf(stderr, "%-*s====>[%s], %s():line %d.\n", \
(windows_width - (_fmt_pos)), "", __SHORT_FILE__, __func__, __LINE__);\
}\
} while(0)

#define ALGO_DEMO(no, back, pttn, pttn_len, fmt, ...) \
printf(" %*s\n", (int)(no+1), pttn); \
printf(" %*s" fmt, (int)(no), "", ## __VA_ARGS__);

#define ALGO_cursor(no, back, pttn_len, fmt, ...) \
printf(" %*s" fmt, (int)(no-(back)), "", ## __VA_ARGS__);
// helper func
// http://stackoverflow.com/questions/7411301/how-to-introduce-date-and-time-in-log-file
char* getFormattedTime(void)
{
    time_t rawtime;
    struct tm* timeinfo;
    
    time(&rawtime);
    timeinfo = localtime(&rawtime);
    
    // Must be static, otherwise won't work
    static char _repr_val[20];
    strftime(_repr_val, sizeof(_repr_val), "%Y-%m-%d %H:%M:%S", timeinfo);
    
    return _repr_val;
}




#define FOR(START, END) \
for (START=0; START < (int)(END); (START)++){
#define FOR2(START, END, STEP) \
for (START=0; START < (int)(END); (START)+=STEP){
#define FOR_DESC(START, END) \
for ((START)=(END-1);START > 0; START--) {
#define END ;}
/*
 * Bad character rule preprocessing table: R1
 */

void init_RL1(int* rl_query_t, const char* pttn, int pttn_len) {
    int i;
    
    FOR(i, ALPHABET_LEN)
        rl_query_t[i] = pttn_len;
    END
    
    FOR(i, pttn_len - 1)
        rl_query_t[pttn[i]] = pttn_len - 1 - i;
    END
}


/*
 * good_suffix
 */
int is_prefix(const char* pttn, int pttn_len, int pos)
{
    int suffix_len = pttn_len - pos;
    // http://www.gnu.org/software/libc/manual/html_node/String_002fArray-Comparison.html
//    if (suffix_len == 0)
//        return 1;
//    else {
        return memcmp(pttn, pttn+pos, suffix_len) == 0;
//    }
}

/*
 * return longest length of good suffix string which ends at pttn[pos]
 */
int suffix_len(const char* pttn, int pttn_len, int pos) {
    int i;
    
    for(i=0; pttn[pos-i] == pttn[pttn_len-1-i] && i < pos;i++);
    return i;
}

void init_RL2(int* rl_query_t, const char* pttn, int pttn_len){
    // i is the position right to the place where a mismtach occurs.
    int i, step=pttn_len;
    
    // case 1: no plausible mtch
    FOR_DESC(i, pttn_len)
        if (is_prefix(pttn, pttn_len, i))
            step = i; // update the step
        // store the val in the first place they are not equal
        rl_query_t[i-1] = step + pttn_len - i; // move the pinter to the right end of the P
    END
    rl_query_t[pttn_len-1] = 0;
    
    // case 2: exist a plausible mtch
    FOR(i, pttn_len)
        int s = suffix_len(pttn, pttn_len, i);
        // satisfying the condition
        if (pttn[i-s] != pttn[pttn_len -1 - s])
            rl_query_t[pttn_len-1-s] = pttn_len - 1 - i + s;//
    END

}

size_t boyer_moore(const char* txt, size_t l, const char* pttn, size_t pttn_len, bool debug){
    int rl1_t[ALPHABET_LEN];
    int* rl2_t = NULL;
    int j,i=pttn_len - 1;
    
    if (pttn_len == 0)
        return NOT_FOUND;
    
    rl2_t = Malloc(int, pttn_len);
    
    // INIT TABLE, CAN BE MOVED OUTSIDE
    init_RL1(rl1_t, pttn, pttn_len);
    init_RL2(rl2_t, pttn, pttn_len);
    
    if (debug)
    {
    printf("string to be matched:\n %s\n", txt);
    printf("begin:\n %s\n %*s\n", pttn, pttn_len, "^");
    }
    
    while (i < l) {
        j = pttn_len - 1;
        while (j >=0 && (txt[i] == pttn[j])){i--;j--;}
        if (j < 0){
            free(rl2_t);
            return i;
        }
        
        if (debug)
        {
        ALGO_cursor(i, 0, pttn_len, "-")
        printf("\n");
        }
        
        i += MAX(rl1_t[txt[i]], rl2_t[j]);
        
        if (debug)
        {
        ALGO_DEMO(i, pttn_len - 1 - j, pttn, pttn_len, "^")
        printf("\n");
        }
    }
    free(rl2_t);
    return NOT_FOUND;
    
}
