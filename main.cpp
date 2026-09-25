#include "Hash_table.h"
#include <fstream>
#include <iostream>

int main() {
    Hash_table<int, std::string> ht(5, 3, 0.5);

    std::ofstream trace("trace.json");
    trace << "[\n";

    ht.insert(10, "A");
    trace << "  {\"action\": \"insert\", \"key\": 10, \"val\": \"A\", \"bucket\": " << (10 % 5) << "},\n";

    ht.insert(15, "B");
    trace << "  {\"action\": \"insert\", \"key\": 15, \"val\": \"B\", \"bucket\": " << (15 % 5) << "},\n";

    ht.insert(7, "C");
    trace << "  {\"action\": \"insert\", \"key\": 7, \"val\": \"C\", \"bucket\": " << (7 % 5) << "}\n";

    trace << "]\n";
    trace.close();

    std::cout << "¡Tabla Hash ejecutada y trace.json generado con exito!" << std::endl;
    return 0;
}