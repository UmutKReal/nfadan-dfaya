import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

class NFAtoDFA:
    def __init__(self, nfa, alphabet, start_state, final_states):
        """
        NFA'dan DFA'ya dönüşümünü gerçekleştiren sınıf.
        """
        self.nfa = nfa  # NFA'nın geçiş fonksiyonu
        self.alphabet = alphabet  # Alfabe
        self.start_state = start_state  # NFA'nın başlangıç durumu
        self.final_states = final_states  # NFA'nın final durumları
        self.dfa = {}  # DFA geçiş fonksiyonu
        self.dfa_start_state = tuple(self.epsilon_closure([start_state]))  # DFA'nın başlangıç durumu
        self.dfa_final_states = []  # DFA'nın final durumları
        self.state_map = {}  # NFA'dan DFA'ya durum haritası
        self.visited = set()  # Ziyaret edilen durumlar

    def epsilon_closure(self, states):
        """
        Bir durum kümesinin epsilon kapanışını hesaplar.
        """
        closure = set(states)
        stack = list(states)
        
        while stack:
            state = stack.pop()
            if 'epsilon' in self.nfa[state]:  # Eğer epsilon geçişi varsa
                for next_state in self.nfa[state]['epsilon']:
                    if next_state not in closure:
                        closure.add(next_state)
                        stack.append(next_state)
        return closure

    def convert(self):
        """
        NFA'dan DFA'ya dönüşüm işlemi.
        """
        unprocessed = [self.dfa_start_state]  # İşlenmemiş durumlar
        while unprocessed:
            current_state = unprocessed.pop()  # İşlenecek bir durum al
            if current_state in self.visited:
                continue
            self.visited.add(current_state)  # Durumu ziyaret et

            # Bu durum kümesi için geçiş fonksiyonları oluşturulacak
            self.dfa[current_state] = {}
            for symbol in self.alphabet:
                next_states = set()
                # Her bir durumdan geçiş hesapla
                for state in current_state:
                    if symbol in self.nfa[state]:
                        next_states.update(self.nfa[state][symbol])

                if next_states:
                    # Epsilon kapanışını al
                    epsilon_closure_states = self.epsilon_closure(list(next_states))
                    self.dfa[current_state][symbol] = tuple(epsilon_closure_states)
                    
                    # Bu yeni durumu işlenmemişler listesine ekle
                    if tuple(epsilon_closure_states) not in self.visited:
                        unprocessed.append(tuple(epsilon_closure_states))

            # Eğer bu durum kümesinde bir final durum varsa, DFA'nın final durumu olmalı
            if any(state in self.final_states for state in current_state):
                self.dfa_final_states.append(current_state)

    def get_dfa(self):
        """
        DFA geçiş fonksiyonunu ve final durumları döndürür.
        """
        return self.dfa, self.dfa_final_states

    def print_dfa(self):
        """
        DFA'nın geçiş tablosunu ve final durumlarını yazdırır.
        """
        print("DFA Geçiş Tablosu:")
        for state, transitions in self.dfa.items():
            print(f"Durum: {state}")
            for symbol, next_state in transitions.items():
                print(f"  {symbol} -> {next_state}")
        
        print("\nDFA Final Durumlar:", self.dfa_final_states)

    def visualize_dfa(self):
        """
        DFA'yı görselleştirmek için yardımcı fonksiyon.
        """
        G = nx.DiGraph()
        
        # Durumlar arası geçişleri ve final durumlarını ekle
        for state, transitions in self.dfa.items():
            for symbol, next_state in transitions.items():
                G.add_edge(state, next_state, label=symbol)
        
        pos = nx.spring_layout(G)
        labels = nx.get_edge_attributes(G, 'label')
        
        # DFA'nın durumlarını ve geçişlerini çiz
        plt.figure(figsize=(10, 8))
        nx.draw(G, pos, with_labels=True, node_size=2000, node_color="skyblue", font_size=15, font_weight="bold")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        plt.title("DFA Geçiş Grafiği")
        plt.show()

    def visualize_nfa(self):
        """
        NFA'yı görselleştiren fonksiyon.
        """
        G = nx.DiGraph()
        
        # Durumlar arası geçişleri ekle
        for state, transitions in self.nfa.items():
            for symbol, next_states in transitions.items():
                if symbol != 'epsilon':
                    for next_state in next_states:
                        G.add_edge(state, next_state, label=symbol)
                else:
                    # epsilon geçişlerini ekle
                    for next_state in next_states:
                        G.add_edge(state, next_state, label="ε")
        
        pos = nx.spring_layout(G)
        labels = nx.get_edge_attributes(G, 'label')
        
        # NFA'nın durumlarını ve geçişlerini çiz
        plt.figure(figsize=(10, 8))
        nx.draw(G, pos, with_labels=True, node_size=2000, node_color="lightgreen", font_size=15, font_weight="bold")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        plt.title("NFA Geçiş Grafiği")
        plt.show()

# NFA'nın Temsili (Daha karmaşık bir örnek)
nfa = {
     0: {'epsilon': [1], 'a': [0, 1]},
    1: {'epsilon': [2], 'b': [2]},
    2: {'b': [3], 'epsilon': [4]},
    3: {'a': [3], 'b': [4]},
    4: {'epsilon': [5], 'a': [2]},
    5: {'b': [5]},

}

# NFA'nın Başlangıç ve Final Durumları
start_state = 0
final_states = {3}

# Alfabe
alphabet = ['a', 'b',]

# NFA'dan DFA'ya dönüşüm
converter = NFAtoDFA(nfa, alphabet, start_state, final_states)

# NFA'yı görselleştir
converter.visualize_nfa()

# DFA'ya dönüşüm işlemi
converter.convert()

# DFA'yı yazdır
converter.print_dfa()

# DFA'yı görselleştir
converter.visualize_dfa()

print("selam")

print("2.commit atılacak kısım")