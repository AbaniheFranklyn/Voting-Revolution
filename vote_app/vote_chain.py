import hashlib
import datetime

class vote:
    def __init__(self, index, timmestamp, vote_data, previous_hash):
        self.index = index
        self.timestamp = timmestamp
        self.vote_data = vote_data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(str(self.index).encode('utf-8')+
                   str(self.timestamp).encode('utf-8')+
                   str(self.vote_data).encode('utf-8')+
                   str(self.previous_hash).encode('utf-8'))
        return sha.hexdigest()
    
class VoteChain:
    def __init__(self):
        self.chain= [self.create_genesis_vote()]
    
    def create_genesis_vote(self):
        return vote(0, datetime.datetime.now(), "Genesis Block", "0")
    
    def get_latest_vote(self):
        return self.chain[-1]
            
    
    def add_vote(self,new_vote):
        new_vote.previous_hash = self.get_latest_vote().hash
        new_vote.hash = new_vote.calculate_hash()
        self.chain.append(new_vote)

    def is_vote_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_vote = self.chain[i]
            previous_vote = self.chain[i-1]
            if current_vote.hash != current_vote.calculate_hash():
                return False
            if current_vote.previous_hash != previous_vote.hash:
                return False
        return True
#votechain = VoteChain()
#for i in range(0,5):
# def adding_vote(index,vin,vote_pary,state,lg):
     votechain.add_vote(vote(index, datetime.datetime.now( ),{"vin":vin, "vote_party":vote_pary,"state":state,
#     "lg":lg}, ""))
# for block in votechain.chain[1:]:
#     print("Block: ", block.index)
#     print("Timestamp: ", block.timestamp)
#     print("Data: ", block.vote_data)
#     print("Hash: ", block.hash)
#     print("Previous Hash: ", block.previous_hash)
#     print("------------")
# result = {'APC':0 ,'PDP':0 }
# for block in votechain.chain[1:]:
#     print("Block: ", block.index)
#     print("Timestamp: ", block.timestamp)
#     print("Data: ", block.vote_data)
#     print("Hash: ", block.hash)
#     print("Previous Hash: ", block.previous_hash)
#     print("------------")
#     r = []
#     z = str(block.vote_data)
#     r.append(z)
#     for i in r:
#         if "APC" in i:
#             result["APC"] += 1
#         elif 'PDP' in i:
#             result["PDP"] += 1
# print("Is blockchain valid? ", votechain.is_vote_chain_valid())
# print(result)

# # a = {'choice':'APC','AGE':'190'}
# # print(a['choice'])
