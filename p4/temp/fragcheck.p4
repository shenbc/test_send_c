#ifndef _FRAGCHECK_
#define _FRAGCHECK_
#include "types.p4"
#include "headers.p4"


control Fragcheck(
    in b32_t gradient_index_in,
    out b32_t gradient_index_out,
    in metadata_t meta) {

    Register<b32_t, index_t>(NUM_REGISTER) gradient_index;

    RegisterAction<b32_t, index_t, b32_t>(gradient_index) write_read_id = {
        void apply(inout b32_t value, out b32_t out_value) {
            if(value == 0){    // unused
                value = gradient_index_in;
                out_value = value;
            }
            else{
                out_value = value;
            }
        }
    };

    RegisterAction<b32_t, index_t, b32_t>(gradient_index) reset_id = {
        void apply(inout b32_t value, out b32_t out_value) {
            value = 0;
            out_value = value;
        }
    };
    
    action check_action() {
        gradient_index_out = write_read_id.execute(meta.pool_index);
    }

    action reset_action(){
        gradient_index_out = reset_id.execute(meta.pool_index);
    }

    table check {
        key = {
           // meta.is_aggregation : exact;
           meta.is_ack : exact;
        }
        actions = {
            check_action;
            reset_action;
            NoAction;
        }
        size = 2;
        const entries={
            0: check_action();
            1: reset_action();
        }
        const default_action = NoAction;
    }

    apply {
        check.apply();
    }
}

#endif 