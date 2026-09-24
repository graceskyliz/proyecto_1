//
// Created by utec_alumno on 16/09/2026.
//

#ifndef AED___REPO_ADE_HASH_TABLE_H
#define AED___REPO_ADE_HASH_TABLE_H
#include <iostream>
#include <functional>
#include <stdexcept>
#include <random>
#include <string>
#include <cmath>

using namespace std;

// HASH BASE
// Convierte cualquier Key en un size_t usando std::hash
template <typename Key>
size_t base_hash(const Key& key) {
    return std::hash<Key>{}(key);
}
template <typename Key>
class DivisionHash {
public:
    size_t operator()(const Key& key, size_t tableSize) const {
        return base_hash(key) % tableSize;
    }
};


template <typename Key, typename Value, typename HashPolicy = DivisionHash<Key>>
class Hash_table {
    struct Node {
        Key key;
        Value value;
        Node* next;

        Node(const Key& k, const Value& v, Node* n = nullptr)
            : key(k), value(v), next(n) {}
    };

    Node** table;               // arreglo de punteros a listas
    size_t capacity;            // tamaño de la tabla
    size_t numElements;         // número total de elementos
    size_t maxCollisionK;       // k del PDF
    double maxFillFactor;       // 0.5
    HashPolicy hashFunction;

    // Libera todos los nodos
    void clearBuckets() {
        for (size_t i = 0; i < capacity; ++i) {
            Node* current = table[i];
            while (current != nullptr) {
                Node* temp = current;
                current = current->next;
                delete temp;
            }
            table[i] = nullptr;
        }
    }

    void initTable(size_t cap) {
        capacity = cap;
        table = new Node*[capacity];
        for (size_t i = 0; i < capacity; ++i) {
            table[i] = nullptr;
        }
    }

    void insertNodeAtHead(const Key& key, const Value& value) {
        size_t index = hashFunction(key, capacity);
        Node* newNode = new Node(key, value, table[index]);
        table[index] = newNode;
        ++numElements;
    }

    // Rehash: duplica capacidad y reubica todos los elementos
    void rehash() {
        size_t oldCapacity = capacity;
        Node** oldTable = table;

        initTable(capacity * 2);
        numElements = 0;

        for (size_t i = 0; i < oldCapacity; ++i) {
            Node* current = oldTable[i];
            while (current != nullptr) {
                insertNodeAtHead(current->key, current->value);
                Node* temp = current;
                current = current->next;
                delete temp;
            }
        }

        delete[] oldTable;
    }

    // Decide si, después de insertar uno más, se supera el fill factor
    bool needsRehashAfterNextInsertion() const {
        double projectedFill =
            static_cast<double>(numElements + 1) /
            static_cast<double>(capacity * maxCollisionK);

        return projectedFill > maxFillFactor;
    }

public:
    explicit Hash_table(size_t initialCapacity = 5,
                       size_t k = 3,
                       double maxFF = 0.5,
                       const HashPolicy& hp = HashPolicy())
        : table(nullptr),
          capacity(0),
          numElements(0),
          maxCollisionK(k),
          maxFillFactor(maxFF),
          hashFunction(hp) {
        if (initialCapacity == 0) {
            throw invalid_argument("La capacidad inicial debe ser > 0");
        }
        if (k == 0) {
            throw invalid_argument("k debe ser > 0");
        }
        if (maxFF <= 0.0) {
            throw invalid_argument("maxFillFactor debe ser > 0");
        }

        initTable(initialCapacity);
    }

    ~HashTable() {
        clearBuckets();
        delete[] table;
    }

    HashTable(const HashTable&) = delete;
    HashTable& operator=(const HashTable&) = delete;

    void insert(const Key& key, const Value& value) {
        size_t index = hashFunction(key, capacity);
        // Si ya existe, actualizamos
        Node* current = table[index];
        while (current != nullptr) {
            if (current->key == key) {
                current->value = value;
                return;
            }
            current = current->next;
        }
        // Verificamos rehash antes de insertar nuevo elemento
        if (needsRehashAfterNextInsertion()) {
            rehash();
            index = hashFunction(key, capacity);
        }

        // Inserción en cabeza
        Node* newNode = new Node(key, value, table[index]);
        table[index] = newNode;
        ++numElements;
    }

    Value* search(const Key& key) {
        size_t index = hashFunction(key, capacity);
        Node* current = table[index];

        while (current != nullptr) {
            if (current->key == key) {
                return &(current->value);
            }
            current = current->next;
        }
        return nullptr;
    }

    const Value* search(const Key& key) const {
        size_t index = hashFunction(key, capacity);
        Node* current = table[index];

        while (current != nullptr) {
            if (current->key == key) {
                return &(current->value);
            }
            current = current->next;
        }
        return nullptr;
    }

    // REMOVE
    bool remove(const Key& key) {
        size_t index = hashFunction(key, capacity);
        Node* current = table[index];
        Node* prev = nullptr;

        while (current != nullptr) {
            if (current->key == key) {
                if (prev == nullptr) {
                    table[index] = current->next;
                } else {
                    prev->next = current->next;
                }
                delete current;
                --numElements;
                return true;
            }
            prev = current;
            current = current->next;
        }

        return false;
    }

    // Utilidades
    bool contains(const Key& key) const {
        return search(key) != nullptr;
    }

    size_t size() const {
        return numElements;
    }

    size_t getCapacity() const {
        return capacity;
    }

    size_t getK() const {
        return maxCollisionK;
    }

    double getFillFactor() const {
        // Fórmula del PDF:
        // FillFactor = #elements / (capacity * k)
        return static_cast<double>(numElements) /
               static_cast<double>(capacity * maxCollisionK);
    }

    double getMaxFillFactor() const {
        return maxFillFactor;
    }

    bool empty() const {
        return numElements == 0;
    }

    // Longitud de la lista en un bucket específico
    size_t bucketSize(size_t index) const {
        if (index >= capacity) {
            throw out_of_range("Índice de bucket fuera de rango");
        }

        size_t count = 0;
        Node* current = table[index];
        while (current != nullptr) {
            ++count;
            current = current->next;
        }
        return count;
    }
    // Imprimir tabla
    void print() const {
        cout << "-----------------------------------------\n";
        cout << "Capacity      : " << capacity << "\n";
        cout << "Elements      : " << numElements << "\n";
        cout << "k             : " << maxCollisionK << "\n";
        cout << "FillFactor    : " << getFillFactor() << "\n";
        cout << "MaxFillFactor : " << maxFillFactor << "\n";
        cout << "-----------------------------------------\n";

        for (size_t i = 0; i < capacity; ++i) {
            cout << "[" << i << "] -> ";
            Node* current = table[i];
            while (current != nullptr) {
                cout << "(" << current->key << ", " << current->value << ") -> ";
                current = current->next;
            }
            cout << "nullptr\n";
        }
        cout << "-----------------------------------------\n";
    }

};
#endif //AED___REPO_ADE_HASH_TABLE_H
