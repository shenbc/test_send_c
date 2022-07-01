## Usage

### Generate the Binary Files

Run `gcc -c send.c -o send.o` to generate the binary file, then run `gcc -shared -o send.so send.o` to generate the shared file invoked by the python files.

### Run Test Scripts

In the root directory of the project, run `python3 tests/send.py`.
