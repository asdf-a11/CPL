#pragma once
#include <type_traits>  // for std::enable_if_t and std::is_integral
#include <cstdint> 
template<class T>
struct CPLPtr{
    union{
        char* ptr;
        unsigned long long value;
    };

    CPLPtr(){}
    CPLPtr(void* ptr){
        this->ptr = (char*)ptr;
    }

    //template<class K, typename = std::enable_if_t<std::is_integral<K>::value>>
    void operator=(void* value){
        ptr = (char*)value;
    }
    void operator=(unsigned long long value){
        ptr = (char*)value;
    }
    template<class K>
    void operator=(CPLPtr<K> value){
        ptr = value.ptr;
    }

    T& operator*(){
        return *((T*)ptr);
    }
    template<class K>
    CPLPtr<T> operator+ (CPLPtr<K> b){
        CPLPtr<T> o;
        o.ptr = nullptr;
        o.value = value + b.value;
        return o;
    }
    T** operator&(){
        return (T**)&ptr;
    }
};

template<class T>
CPLPtr<T> operator+(CPLPtr<T> a , int b){
    CPLPtr<T> o;
    o.ptr = nullptr;
    o.value = a.value + b;
    return o;
}

template<class T>
CPLPtr<T> operator+(int b, CPLPtr<T> a){
    CPLPtr<T> o;
    o.ptr = nullptr;
    o.value = a.value + b;
    return o;
}