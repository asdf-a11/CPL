#pragma once
#include <iostream>

template<class T>
class CPL_LIST{
private:
    T* dataList = nullptr;
    int size;
public:

    CPL_LIST(int size){
        this->dataList = new T[size];
        this->size = size;
    }

    T& operator[](int position){
        #ifdef SAFE
            if(position >= size || position < 0){
                std::cerr << "Invalid list index pos=" << position << "!!!!\n";
            }
        #endif
        return dataList[position];
    }

    void operator=(T value){
        for(int i = 0; i < size; i++){
            dataList[i] = value;
        }
    }
    #define C(op) \
        template<class U>\
        CPL_LIST<T> operator op (U value){\
            CPL_LIST<T> ret(size);\
            for(int i = 0; i < size; i++){\
                ret.dataList[i] = dataList[i] op value;\
            }\
            return ret;\
        }

    C(+);
    C(*);
    C(-);
    C(/);

    #undef c

    T* operator&(){
        return dataList;
    }

    ~CPL_LIST(){
        delete[] dataList;
    }
};