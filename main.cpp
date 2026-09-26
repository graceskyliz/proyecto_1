#include "Hash_table.h"
#include <fstream>
#include <iostream>
#include <string>

void emitEvent(std::ofstream& trace, const std::string& action, int key,
           const std::string& value, size_t bucket, bool result,
           const std::string& detail, size_t capacity) {
    static bool first = true;
    if (!first) trace << ",\n";
    first = false;
    trace << "  {\"action\": \"" << action << "\", \"key\": " << key
        << ", \"val\": \"" << value << "\", \"bucket\": " << bucket
        << ", \"result\": " << (result ? "true" : "false")
        << ", \"detail\": \"" << detail << "\", \"capacity\": "
        << capacity << "}";
}

int main() {
    Hash_table<int, std::string> ht(5, 3, 0.5);

    std::ofstream trace("trace.json");
    trace << "[\n";

    ht.insert(10, "A");
    emitEvent(trace, "insert", 10, "A", ht.bucketIndex(10), true, "insertado", ht.getCapacity());
    ht.insert(15, "B");
    emitEvent(trace, "insert", 15, "B", ht.bucketIndex(15), true, "insertado", ht.getCapacity());
    ht.insert(7, "C");
    emitEvent(trace, "insert", 7, "C", ht.bucketIndex(7), true, "insertado", ht.getCapacity());

    ht.insert(10, "A2");
    emitEvent(trace, "update", 10, "A2", ht.bucketIndex(10), true, "clave existente actualizada", ht.getCapacity());

    const auto found = ht.search(15);
    emitEvent(trace, "search", 15, found ? *found : "", ht.bucketIndex(15), found != nullptr,
              found ? "encontrado" : "no encontrado", ht.getCapacity());
    const auto missing = ht.search(99);
    emitEvent(trace, "search", 99, "", ht.bucketIndex(99), missing != nullptr,
              missing ? "encontrado" : "no encontrado", ht.getCapacity());

    emitEvent(trace, "contains", 7, "", ht.bucketIndex(7), ht.contains(7),
              ht.contains(7) ? "pertenece" : "no pertenece", ht.getCapacity());
    emitEvent(trace, "bucketSize", 15, "", ht.bucketIndex(15), true,
              std::to_string(ht.bucketSize(ht.bucketIndex(15))), ht.getCapacity());
    emitEvent(trace, "size", 0, "", 0, true, std::to_string(ht.size()), ht.getCapacity());
    emitEvent(trace, "getCapacity", 0, "", 0, true, std::to_string(ht.getCapacity()), ht.getCapacity());
    emitEvent(trace, "getK", 0, "", 0, true, std::to_string(ht.getK()), ht.getCapacity());
    emitEvent(trace, "getFillFactor", 0, "", 0, true, std::to_string(ht.getFillFactor()), ht.getCapacity());
    emitEvent(trace, "getMaxFillFactor", 0, "", 0, true, std::to_string(ht.getMaxFillFactor()), ht.getCapacity());
    emitEvent(trace, "empty", 0, "", 0, ht.empty(), ht.empty() ? "vacia" : "no vacia", ht.getCapacity());

    const bool removed = ht.remove(15);
    emitEvent(trace, "remove", 15, "B", ht.bucketIndex(15), removed,
              removed ? "eliminado" : "no encontrado", ht.getCapacity());
    const bool removedMissing = ht.remove(99);
    emitEvent(trace, "remove", 99, "", ht.bucketIndex(99), removedMissing,
              removedMissing ? "eliminado" : "no encontrado", ht.getCapacity());

    for (int key = 20; key <= 26; ++key) {
        std::string value(1, static_cast<char>('D' + key - 20));
        ht.insert(key, value);
        emitEvent(trace, "insert", key, value, ht.bucketIndex(key), true,
                  "insertado", ht.getCapacity());
    }
    ht.print();
    emitEvent(trace, "print", 0, "", 0, true, "tabla impresa en consola", ht.getCapacity());

    trace << "]\n";
    trace.close();

    std::cout << "¡Tabla Hash ejecutada y trace.json generado con exito!" << std::endl;
    return 0;
}