#ifndef HEADERS_P4
#define HEADERS_P4

#include "types.p4"

header ethernet_h {
    mac_addr_t dst_addr;
    mac_addr_t src_addr;
    bit<16>   ether_type;
}

header ipv4_h {
    bit<4>    version;
    bit<4>    ihl;
    bit<8>    diffserv;
    bit<16>   total_len;
    bit<16>   identification;
    bit<3>    flags;
    bit<13>   frag_offset;
    bit<8>    ttl;
    bit<8>    protocol;
    bit<16>   hdr_checksum;
    ipv4_addr_t src_addr;
    ipv4_addr_t dst_addr;
}

header lina_h {
    bit<8>  switch_id;
    b32_t worker_bitmap;
    bit<4>  count;
    bit<4>  is_collision;
    b32_t tensor_index;
    b32_t aggregator_index;
}

header payload_h {
    data_t value00;
    data_t value01;
    data_t value02;
    data_t value03;
    data_t value04;
    data_t value05;
    data_t value06;
    data_t value07;
    data_t value08;
    data_t value09;
    data_t value10;
    data_t value11;
    data_t value12;
    data_t value13;
    data_t value14;
    data_t value15;
    data_t value16;
    data_t value17;
    data_t value18;
    data_t value19;
    data_t value20;
    data_t value21;
    data_t value22;
    data_t value23;
    data_t value24;
    data_t value25;
    data_t value26;
    data_t value27;
    data_t value28;
    data_t value29;
    data_t value30;
    data_t value31;
}

struct header_t {
    ethernet_h      ethernet;
    ipv4_h          ipv4;
    lina_h          lina;
    payload_h  tensor;
}

/*************************************************************************
 ***********************  M E T A D A T A  *******************************
 *************************************************************************/
struct empty_metadata_t {}

struct metadata_t {
    bit<1> is_aggregation;
    bit<4>  count;
    bit<4>  is_collision;
    b32_t tensor_index;
    b32_t aggregator_index;
    bit<32>  index;
}


#endif /* HEADERS_P4 */