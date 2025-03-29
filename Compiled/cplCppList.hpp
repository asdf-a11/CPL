#pragma once
template<class T>
struct CPL_LIST{
    T* dataList = nullptr;
    int size;
    CPL_LIST(int size){
        dataList = new T[size];
        this->size = size;
    }

    T& operator[](int position){
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

    ~CPL_LIST(){
        delete[] dataList;
    }
};