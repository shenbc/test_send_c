/* -*- P4_16 -*- */
#include <core.p4>
#include <tna.p4>
#include "parser.p4"
#include "headers.p4"
#include "processor.p4"
#include "types.p4"
#include "config.p4"
#include "fragcheck.p4"

control Ingress(
        inout header_t hdr,
        inout metadata_t ig_md,
        in ingress_intrinsic_metadata_t ig_intr_md,
        in ingress_intrinsic_metadata_from_parser_t ig_prsr_md,
        inout ingress_intrinsic_metadata_for_deparser_t ig_dprsr_md,
        inout ingress_intrinsic_metadata_for_tm_t ig_tm_md) {
    
    action set_agg() {
        ig_md.is_aggregation = 1;
    }

    action unset_agg() {
        ig_md.is_aggregation = 0;
    }
    
    table switch_check {
        key = {
            hdr.lina.switch_id: exact;
        }
        actions = {
            set_agg;
            unset_agg;
        }
        size = 1;
        default_action = unset_agg;
    }
   
    action drop() {
        ig_dprsr_md.drop_ctl = 1;
    }
    
    action ipv4_forward(mac_addr_t dst_addr, egress_spec_t port) {
        ig_tm_md.ucast_egress_port = port;
        // hdr.ethernet.src_addr = hdr.ethernet.dst_addr;
        // hdr.ethernet.dst_addr = dst_addr;
        // hdr.ipv4.ttl = hdr.ipv4.ttl - 1;
    }
    
    table ipRoute {
        key = {
            hdr.ipv4.dst_addr: exact;
        }
        actions = {
            ipv4_forward;
            drop;
            NoAction;
        }
        size = 1<<8;
        default_action = drop;
    }


    Register<bit<8>,index_t>(NUM_REGISTER, 0) count_reg; 
    
    // RegisterAction<bit<8>, index_t, bit<8>>(count_reg) read_add_count = {
    //     void apply(inout bit<8> value, out bit<8> read_value) {
    //         value = value+1;
            
    //         if(value == hdr.lina.count){
    //             value=0;
    //             read_value = value;
    //         }
    //         else{
    //             read_value = value;
    //         }
    //     }
    // };
    RegisterAction<bit<4>, index_t, bit<4>>(count_reg) read_add_count = {
        void apply(inout bit<4> value, out bit<4> read_value) {
            value = value+1;
            
            if(value == hdr.lina.count){
                value=0;
                read_value = value;
            }
            else{
                read_value = value;
            }
        }
    };

    action add_count_action(){
        ig_md.count=read_add_count.execute(ig_md.index);
    }

    Fragcheck() frag_check;

    Processor() value00;
    Processor() value01;
    Processor() value02;
    Processor() value03;
    Processor() value04;
    Processor() value05;
    Processor() value06;
    Processor() value07;
    Processor() value08;
    Processor() value09;
    Processor() value10;
    Processor() value11;
    Processor() value12;
    Processor() value13;
    Processor() value14;
    Processor() value15;
    Processor() value16;
    Processor() value17;
    Processor() value18;
    Processor() value19;
    Processor() value20;
    Processor() value21;
    Processor() value22;
    Processor() value23;
    Processor() value24;
    Processor() value25;
    Processor() value26;
    Processor() value27;
    Processor() value28;
    Processor() value29;
    Processor() value30;
    Processor() value31;

    apply {
        if(hdr.lina.isValid()) {
            switch_check.apply();
            
            if(ig_md.is_aggregation == 1 ){
                ig_md.aggregator_index = hdr.lina.aggregator_index;

                //TODO: Given aggregator index, return tensor index in the specific register.
                frag_check.apply(ig_md.tensor_index,ig_md); 

                if (ig_md.tensor_index == hdr.lina.tensor_index){
                    add_count_action(); 

                    value00.apply(hdr.tensor.value00,hdr.tensor.value00,ig_md);
                    value01.apply(hdr.tensor.value01,hdr.tensor.value01,ig_md);
                    value02.apply(hdr.tensor.value02,hdr.tensor.value02,ig_md);
                    value03.apply(hdr.tensor.value03,hdr.tensor.value03,ig_md);
                    value04.apply(hdr.tensor.value04,hdr.tensor.value04,ig_md);
                    value05.apply(hdr.tensor.value05,hdr.tensor.value05,ig_md);
                    value06.apply(hdr.tensor.value06,hdr.tensor.value06,ig_md);
                    value07.apply(hdr.tensor.value07,hdr.tensor.value07,ig_md);
                    value08.apply(hdr.tensor.value08,hdr.tensor.value08,ig_md);
                    value09.apply(hdr.tensor.value09,hdr.tensor.value09,ig_md);
                    value10.apply(hdr.tensor.value10,hdr.tensor.value10,ig_md);
                    value11.apply(hdr.tensor.value11,hdr.tensor.value11,ig_md);
                    value12.apply(hdr.tensor.value12,hdr.tensor.value12,ig_md);
                    value13.apply(hdr.tensor.value13,hdr.tensor.value13,ig_md);
                    value14.apply(hdr.tensor.value14,hdr.tensor.value14,ig_md);
                    value15.apply(hdr.tensor.value15,hdr.tensor.value15,ig_md);
                    value16.apply(hdr.tensor.value16,hdr.tensor.value16,ig_md);
                    value17.apply(hdr.tensor.value17,hdr.tensor.value17,ig_md);
                    value18.apply(hdr.tensor.value18,hdr.tensor.value18,ig_md);
                    value19.apply(hdr.tensor.value19,hdr.tensor.value19,ig_md);
                    value20.apply(hdr.tensor.value20,hdr.tensor.value20,ig_md);
                    value21.apply(hdr.tensor.value21,hdr.tensor.value21,ig_md);
                    value22.apply(hdr.tensor.value22,hdr.tensor.value22,ig_md);
                    value23.apply(hdr.tensor.value23,hdr.tensor.value23,ig_md);
                    value24.apply(hdr.tensor.value24,hdr.tensor.value24,ig_md);
                    value25.apply(hdr.tensor.value25,hdr.tensor.value25,ig_md);
                    value26.apply(hdr.tensor.value26,hdr.tensor.value26,ig_md);
                    value27.apply(hdr.tensor.value27,hdr.tensor.value27,ig_md);
                    value28.apply(hdr.tensor.value28,hdr.tensor.value28,ig_md);
                    value29.apply(hdr.tensor.value29,hdr.tensor.value29,ig_md);
                    value30.apply(hdr.tensor.value30,hdr.tensor.value30,ig_md);
                    value31.apply(hdr.tensor.value31,hdr.tensor.value31,ig_md);

                    if (ig_md.count == 0){ // Aggregation done.
                        ipRoute.apply();
                    }
                    else{
                        drop();
                    }
                }
                else{ // Collision
                    hdr.lina.is_collision=1;
                    ipRoute.apply();   
                }
            }
            else{ // Other switches' job.
                ipRoute.apply();
            }
        } 
        else {
            if (hdr.ipv4.isValid()) {
                ipRoute.apply();
            }
            else{
                drop();
            }
        }
    }
}

Pipeline(IngressParser(),
         Ingress(),
         IngressDeparser(),
         EgressParser(),
         Egress(),
         EgressDeparser()) pipe;

Switch(pipe) main;