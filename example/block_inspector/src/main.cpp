
#include <iostream>
#include <vector>
#include <fstream>

#include <PS2Textures.h>

void readFile(std::vector<char>& data, const std::string& file_path)
{
    std::ifstream file(file_path, std::ios::binary | std::ios::ate);

    if (file.is_open()) {
        std::streamsize size = file.tellg();
        file.seekg(0, std::ios::beg);

        data.resize(size);

        if (!file.read(data.data(), size))
        {
            std::cerr << "Error reading file." << std::endl;
        }

        file.close();
    }
    else
    {
        std::cerr << "Error opening file." << std::endl;
    }
}

void writeFile(std::vector<char>& data, const std::string& file_path)
{
    std::ofstream file(file_path, std::ios::binary);

    if (file.is_open())
    {
        file.write(data.data(), data.size());
        file.close();

        std::cout << "Data has been written to the file." << std::endl;
    }
    else
    {
        std::cerr << "Error opening the file for writing." << std::endl;
    }
}

int main()
{
	std::vector<char> data;
	std::vector<char> data2;

	data2.resize(0x8000);

	readFile(data, "../files/gamespy_128x64_block_1.sux");
	
	writeTexPSMT8(0, 0, 0, 0, 128, 64, &(data[0]));
	readTexPSMCT32(0, 0, 0, 0, 64, 32, &(data2[0]));
	
	/*
		Result:
			FD FD FD FD  FD FD FD FD  FD FD FD E7  B0 4B 1A 22
			61 BB EE FD  FD FD FD FD  FD FD FD FD  FD FD FD FD
			
		Expected:
			FD FD FD FD  FD FD FD FD  FD FD FD E7  A8 53 1A 22
			61 BB F6 FD  FD FD FD FD  FD FD FD FD  FD FD FD FD
			
			1011 0000 0100 1011 0001 1010 0010 0010
			1010 1000 0101 0011 0001 1010 0010 0010
			
			0110 0001 1011 1011 1110 1110 1111 1101
			0110 0001 1011 1011 1111 0110 1111 1101
			
	*/
	writeFile(data2, "../files/gamespy_128x64_block_1.sux.2");

	return 0;
}
