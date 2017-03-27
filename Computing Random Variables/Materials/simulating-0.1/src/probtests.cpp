//
//  probtests.cpp
//  KMP
//
//  Created by Wang Yi on 7/3/17.
//  Copyright © 2017 Wang Yi@yiak.co. All rights reserved.
//

#include "probtests.hpp"

#define WINDOWS_WIDTH 30
// think about it, if you use `this` pointer in C++. This is a trick. Hence we want
#define get_address(objref) (&(*objref))
#define memory_move(ref, bytes) (reinterpret_cast<char*>(ref) + (bytes))

using std::accumulate;

#define weights_pos offsetof(alphabet_distribution, m_weights)

// causion, memory manipulation
template <typename _Tp, typename _Ar, class _BinaryOperation>
_Tp*
map_array(_Ar __array, int len, _BinaryOperation __binary_op)
{
    _Tp* ret = Malloc(_Tp, len);
    int i;
    FOR(i, len)
        ret[i] = __binary_op(__array[i]);
    END
    
    return ret;
}


bool is_alphabet(bytes ch_dec)
{
    if ((ch_dec >= 'a' && ch_dec <= 'z') ||
        (ch_dec >= 'A' && ch_dec <= 'Z'))
        return true;
    return false;
}


typedef unsigned char bytes;
bytes
alphabet_distribution::operator()(void)
{
    bytes ch;
    int ch_dec;
    int* weights=nullptr;
    
    std::random_device device;
    std::mt19937 gen(device());
    weights = this->m_weights != nullptr ? this->m_weights : this->_cache_pb;
    
    // refuse sampling has a problem:
    // if there are too much choices to be refused, the programme has a
    // large probability to be blocked. Hence we need to narrow donw the sampling space
    
    
    if ((double)m_vals_range / ALPHABET_LEN > m_threshold)
    {
        std::uniform_int_distribution<unsigned int> random_range(0, ALPHABET_LEN);
        ch_dec = random_range(gen);
        while (not is_alphabet(ch_dec) || weights[ch_dec] <= 0)
        {
            ch_dec = random_range(gen);
        }
    } else {
        // another algorithm
        int ch_dec_id = -1;
        std::uniform_int_distribution<unsigned int> random_range(0, this->m_vals_range - 1);
        // linear mapping
        ch_dec_id = random_range(gen);
        ch_dec = compact_seq[ch_dec_id];
    }
    
    ch = bytes(ch_dec);
    return ch;
}

template <typename _Tp>
const char*
alphabet_distribution::histogram(_Tp hist, const char* fmt, char32_t symbol)
{
    // http://stackoverflow.com/questions/7211923/adding-an-offset-to-a-pointer
    // you might refer to this poster to verify the process of offset to a pointer
    // HERE is my memo for your reference:
    //  lldb debug method:
    //  "read some memory as an array of N elements of type T":
    //  1) memory read -t `type` -c `size` v
    //  2) pointer casting
    //  3) adding a python scripting module http://stackoverflow.com/questions/7062173/view-array-in-lldb-equivalent-of-gdbs-operator-in-xcode-4-1
    //  4) for Xcode 8.0+: parray <COUNT> <EXPRESSION>
    //  5) (lldb) type summary add -s "${var[0-256]}" "int *"
    //      (lldb) frame variable hist
    double* temp = nullptr;
    if (hist == nullptr)
    {
        temp = map_array<double>((int*)(reinterpret_cast<char*>(&(*this)) + weights_pos), m_weights != nullptr ? allocated : ALPHABET_LEN, [this](double curr) {return (double)curr / this->m_vals_range;});
        hist = temp;
    }
    
    string out = "\n **** alphadistribution toolkit -- histogram, copyright © 2017 Wang Yi (yiak.wy@gmail.com) **** \n\n";
    std::stringstream split;
    int i;

    FOR(i, ALPHABET_LEN)
    string temp;
    if (hist[i] <= 0)
        continue;
    out += (boost::format(fmt) % (char)i).str();
    
    std::string row = std::string(hist[i] < 1 ? hist[i] * WINDOWS_WIDTH: hist[i], symbol);
    split << std::setfill(' ') << std::left << std::setw(WINDOWS_WIDTH) << row << hist[i] << std::endl;
    out += split.str();
    // clean the stream reader
    split.str("")
    END

    if (temp != nullptr)
        free(temp);
    
    return out.c_str();
}

// checking whether it is a uniform sampling
// google test for unity testing
bool
alphabet_distribution::test_uniform_checking(int test_cases)
{
    bytes ch;
    int i;
    double avg, utd;
    double* uniform_ret = nullptr;
    
    int* symbol_Table = Malloc(int, ALPHABET_LEN);
    if (symbol_Table == NULL)
        ;
    
    FOR(i, this->m_vals_range)
    symbol_Table[ch] = 0;
    END
    
    for(i=0; i < test_cases; i++){
        ch = (*this)();
        symbol_Table[ch] += 1;
    }
    
    avg = (double)test_cases / m_vals_range;
    utd = sqrt(reduce_array<int*, double>(symbol_Table, ALPHABET_LEN, 0.0,
                            [avg](double pre, int curr){return pre + (curr > 0 ? (curr-avg)*(curr-avg) : 0);}) / double(this->m_vals_range) );

    uniform_ret = map_array<double>(symbol_Table, ALPHABET_LEN,
                            [test_cases](int curr) -> double {return double(curr) / test_cases;});
    LOG(INFO) << "running test cases <" << test_cases << "> : "
                               << "avg:" << avg << " , " << "utd:" << utd << " , " << "ratio of utd over avg" << utd / avg << std::endl
                               << "probability histogram:" << std::endl
                               << histogram<double*>(uniform_ret)
                               << std::endl;
    
    // google test , asserts ...
    free(symbol_Table);
    free(uniform_ret);
    symbol_Table = nullptr;
    return true;
}

