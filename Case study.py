import random, csv, os, time
from itertools import combinations
import string

def create_database(num_transactions=10000, min_items=3, max_items=10):
    
    base_items = [
        "milk","bread","butter","eggs","cheese","apple","banana","orange",
        "chicken","beef","fish","rice","pasta","tomato","onion","garlic",
        "coffee","tea","sugar","salt","oil","yogurt","chips","juice"
    ]

    synthetic_items = [f"item_{c}{i:02d}" for c in string.ascii_uppercase for i in range(1, 6)][:100]
    
    items = base_items + synthetic_items
    
    database = []
    for _ in range(num_transactions):
        # Increased max_items to 10 to create more combinations
        n = random.randint(min_items, max_items)
        transaction = random.sample(items, n)
        database.append(transaction)
    return database

def save_database_csv(database, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["transaction_id", "items"])
        for idx, transaction in enumerate(database, start=1):
            writer.writerow([idx, "|".join(transaction)])

def get_support(itemset, transactions):
   
    count = sum(1 for t in transactions if itemset.issubset(t))
    return count / len(transactions)

def apriori(transactions, min_support=0.002):
    transactions = list(map(set, transactions))
    
   
    all_items = set().union(*transactions)
    C1 = [frozenset([i]) for i in all_items]
    
    
    L1_with_support = {}
    for itemset in C1:
        support = get_support(itemset, transactions)
        if support >= min_support:
            L1_with_support[itemset] = support
    
    frequent_itemsets = list(L1_with_support.keys())
    
    k = 2
    Lk = list(L1_with_support.keys())
    
    while Lk:
       
        Ck_sets = set()
        for i in range(len(Lk)):
            for j in range(i+1, len(Lk)):
                union_set = Lk[i] | Lk[j]
                if len(union_set) == k:
                    
                    subsets_are_frequent = True
                   
                    if k > 2: 
                        for subset in combinations(union_set, k-1):
                            if frozenset(subset) not in Lk:
                                subsets_are_frequent = False
                                break
                    if subsets_are_frequent:
                        Ck_sets.add(union_set)
        
       
        Lk_next = []
        for itemset in Ck_sets:
            support = get_support(itemset, transactions)
            if support >= min_support:
                Lk_next.append(itemset)
        
        Lk = Lk_next
        frequent_itemsets.extend(Lk)
        k += 1
        
       
        if len(frequent_itemsets) >= 1000:
            break
            
    return frequent_itemsets

if __name__ == "__main__":
    num_transactions = 10000 
    min_support_threshold = 0.002 

    
    start_time = time.time()
    database = create_database(num_transactions=num_transactions)
    generation_time = time.time() - start_time
    print(f"✅ Database created with {len(database)} transactions and {len(set().union(*database))} unique items in {generation_time:.2f} seconds.")

   
    os.makedirs("output", exist_ok=True)
    csv_filename = f"output/transactions_{int(time.time())}.csv"
    save_database_csv(database, filename=csv_filename)
    print(f"✅ Database saved to CSV file: {csv_filename}")

    
    start_time = time.time()
    frequent_sets = apriori(database, min_support=min_support_threshold)
    apriori_time = time.time() - start_time

    print(f"\n--- Apriori Results ---")
    print(f"Time to execute Apriori: {apriori_time:.2f} seconds")
    print(f"Minimum Support Threshold: {min_support_threshold * 100}% (Necessary to find 1000+ sets)")
    print(f"✅ Total frequent itemsets found: {len(frequent_sets)}")

    limit = min(1000, len(frequent_sets))
    print(f"\n🔹 Displaying first {limit} frequent itemsets (L1, L2, L3...):\n")
   
    itemset_groups = {}
    for itemset in frequent_sets:
        k = len(itemset)
        if k not in itemset_groups:
            itemset_groups[k] = []
        itemset_groups[k].append(itemset)

    count = 0
    for k in sorted(itemset_groups.keys()):
        print(f"--- L{k} (Size {k} Itemsets) ---")
        for itemset in itemset_groups[k]:
            if count < limit:
                print(f"  {count+1:>4}. Items: {set(itemset)}")
                count += 1
            else:
                break
        if count >= limit:
            break
