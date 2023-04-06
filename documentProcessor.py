from collections import defaultdict





class dynamicIndex:
    
    def __init__(self, payload):
        
        self.documentLocation = []
        self.documentContent = []
        for index, document in enumerate(payload):
            self.documentContent.append(str(index) + " " + document[1])
            self.documentLocation.append(document[0])
            
        self.termIndex = self.mapReduce()
    
    
    
    def mapReduce(self):
        
        intermediate = defaultdict(list)
        for content in self.documentContent:
            for keyWord, *value in self.mapFunction(content):
                intermediate[keyWord].append(value)
        return [(output[0], ', '.join(str(document) for document in output[1])) for index in (self.reduceFunction(keyWord, value) for keyWord, value in intermediate.items()) if index for output in index]
    
    
    
    def mapFunction(self, content):
        
        terms = content.strip().split()
        documentIndex = int(terms[0])
        termCount = defaultdict(int)
        for term in terms[1 : ]:
            termCount[term] += 1
        for term, count in termCount.items():
            yield term, documentIndex, count
    
    
    
    def reduceFunction(self, term, documentCount):
        
        documents = set()
        for documentIndex, count in documentCount:
            documents.add(documentIndex)
        yield term, documents






class termPartitionedIndex:
    
    def __init__(self, payload, numberOfPartitions = 1):
        
        self.documentLocation = []
        self.documentContent = []
        for index, document in enumerate(payload):
            self.documentContent.append(document[1])
            self.documentLocation.append(document[0])
            
        self.termIndex = self.termPartitionedIndexing(numberOfPartitions)
    
    
    
    def termPartitionedIndexing(self, numberOfPartitions):
        
        mappedData = []
        for index, document in enumerate(self.documentContent):
            mappedData.extend(self.mapFunction(index, document))
        
        partitions = self.partitionData(mappedData, numberOfPartitions)
        
        output = []
        for partition in partitions:
            termCount = defaultdict(list)
            for term, documentCount in partition:
                termCount[term].append(documentCount)
            for term, documentCounts in termCount.items():
                output.append(self.reduceFunction(term, documentCounts))
        return output
    
    
    
    def partitionData(self, data, numberOfPartitions):
        
        partitions = [list() for _ in range(numberOfPartitions)]
        for index, item in enumerate(data):
            partitions[index % numberOfPartitions].append(item)
        return partitions
    
    
    
    def mapFunction(self, documentID, document):
        
        counts = defaultdict(int)
        for term in document.split():
            counts[term] += 1
        output = []
        for term, count in counts.items():
            output.append((term, (documentID, count)))
        return output
    
    
    
    def reduceFunction(self, term, documentCounts):
        
        if not documentCounts:
            return (term, 0, [])
        totalCount = sum(count for documentIndex, count in documentCounts)
        return (term, totalCount, documentCounts)
    







if __name__ == '__main__':    
    corpus = [
        [1, 'this is the first document .'],
        [1, 'this is the second document .'],
        [1, 'and this is the third one .'],
        [1, 'is this the first document ?']
    ]

    calling = dynamicIndex(corpus)
    print("Dynamic indexing:\n\n")
    for line in sorted(calling.termIndex):
        print(f"{line[0]}: {line[1]}")
        
        
    calling = termPartitionedIndex(corpus)
    print("\n\n\nTerm-partitioned indexing:\n\n")
    for term, total_count, doc_counts in calling.termIndex:
        if not doc_counts:
            print(f"{term}: total count = {total_count}, documents = []")
        else:
            doc_indexes = ', '.join(str(doc_index) for doc_index, count in doc_counts)
            print(f"{term}: total count = {total_count}, documents = [{doc_indexes}]")