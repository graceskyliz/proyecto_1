#include "HashTable.h"
#include <fstream>

int main() {
    std::ofstream trace("trace.json");
    trace << "[\n";

    // Se puede registrar eventos conforme usas tu estructura:
    // {"action": "insert", "key": 8, "val": "A", "bucket": 0, "collision": false}
    // {"action": "insert", "key": 12, "val": "B", "bucket": 0, "collision": true}
    // {"action": "rehash", "old_cap": 4, "new_cap": 8}

    trace << "  {\"action\": \"insert\", \"key\": 8, \"val\": \"A\", \"bucket\": 0},\n";
    trace << "  {\"action\": \"insert\", \"key\": 12, \"val\": \"B\", \"bucket\": 0}\n";
    trace << "]\n";
    return 0;
}