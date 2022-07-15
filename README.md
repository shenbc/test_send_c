## Packet Format

| Ethernet | IPv4 | LINA | Payload |
|--|--|--|--|

Specifically, LINA contains:

* 8-bit switch_id
* 32-bit worker_bitmap
* 4-bit count: decide when to finish aggregation
* 4-bit is_collision
* 32-bit tensor_index: the index of the start tensor in given gradient
* 32-bit aggregator_index: the index of allocated aggregator (register) for this packet

Payload contains 32 32-bit tensors.

## Usage

### Generate the Binary Files

Run `./compile.sh` to compile `send.c` and generate the shared files.

### Run Test Scripts

Run `sudo python3 tests/send.py`.
