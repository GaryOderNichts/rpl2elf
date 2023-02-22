.PHONY: rpl2elf clean

rpl2elf:
	g++ *.cpp external/fmt/*.cpp -I include -I external/fmt/include -I external/excmd/include -o rpl2elf -lz

clean:
	rm rpl2elf
