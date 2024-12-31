struct cvorListe;
typedef struct cvorListe* Pozicija;
typedef struct cvorListe** Lista;
typedef struct cvorListe {
	int HIme;
	int HLozinka;
	Pozicija next;
}Cvor;

struct Hash;
typedef struct Hash* PozicijaHash;
typedef struct Hash {
	int velicina;
	Lista NizCvorova;
}HashT;

int InitTablice(PozicijaHash,int);
int Hash(const char[]);
int SljedeciPrBr(int);
int DodajUHashTab(const char [], const char [], PozicijaHash);
int BrisiUHashTab(const char[], const char[], PozicijaHash);
bool JeLiUHashTab(const char[], const char[], PozicijaHash);
int IzbrisiSveUHashTab(PozicijaHash);

int InitTablice(PozicijaHash Tab,int vel) {
	Tab->velicina = SljedeciPrBr(vel);
	Tab->NizCvorova = NULL;
	Tab->NizCvorova = (Lista)malloc(Tab->velicina * sizeof(Pozicija));
	if (Tab->NizCvorova == NULL) {
		free(Tab);
		printf("Greska u alociranju memorije...\n");
		return NULL;
	}
	for (int i = 0; i < Tab->velicina; i++) {
		Tab->NizCvorova[i] = NULL;
	}
	return EXIT_SUCCESS;
}

int DodajUHashTab(const char korIme[],const char lozinka[], PozicijaHash Tab) {
	int HLozinka = Hash(lozinka);
	int HIme = Hash(korIme);
	Pozicija novi = NULL;
	novi = (Pozicija)malloc(sizeof(Cvor));
	if (novi == NULL) {
		printf("Greska u alokaciji memorije...");
		return EXIT_FAILURE;
	}
	novi->HIme = HIme;
	novi->HLozinka = HLozinka;
	novi->next = Tab->NizCvorova[HLozinka % Tab->velicina];
	Tab->NizCvorova[HLozinka % Tab->velicina] = novi;
	return EXIT_SUCCESS;
}

int SljedeciPrBr(int a) {
	int br = 0;
	if (a <= 1) {
		return 2;
	}
	if (a == 4) {
		return 5;
	}
	while (true) {
		for (int i = 2; i < a / 2; i++) {
			if (a % i == 0) {
				br++;
			}
		}
		if (br == 0) {
			break;
		}
		else {
			br = 0;
			a++;
		}
	}
	return a;
}

int Hash(const char str[]) {
	int Ret=0;
	int i = 1;
	while (*str != '\0') {
		Ret += *str++*i++;
	}
	Ret += 245; //salt
	return Ret;
}

bool JeLiUHashTab(const char korIme[], const char lozinka[], PozicijaHash Tab) {
	Pozicija temp = Tab->NizCvorova[Hash(lozinka) % Tab->velicina];
	while (temp != NULL) {
		if (temp->HIme == Hash(korIme) && temp->HLozinka == Hash(lozinka)) {
			return true;
		}
		temp = temp->next;
	}
	return false;
}

int BrisiUHashTab(const char korIme[], const char lozinka[], PozicijaHash Tab) {
	if (!JeLiUHashTab(korIme, lozinka, Tab)) {
		printf("Nije pronaden u H tablici...\n");
		return EXIT_FAILURE;
	}
	Pozicija temp = Tab->NizCvorova[Hash(lozinka) % Tab->velicina];
	if (temp->HIme == Hash(korIme) && temp->HLozinka == Hash(lozinka)) {
		Tab->NizCvorova[Hash(lozinka) % Tab->velicina] = temp->next;
		free(temp);
		return EXIT_SUCCESS;
	}
	while (temp->next != NULL) {
		if (temp->next->HIme == Hash(korIme) && temp->next->HLozinka == Hash(lozinka)) {
			break;
		}
		temp = temp->next;
	}
	Pozicija br = temp->next;
	temp->next = br->next;
	free(br);
	return EXIT_SUCCESS;
}

int IzbrisiSveUHashTab(PozicijaHash Tab) {
	Pozicija temp;
	Pozicija next;
	for (int i = 0; i < Tab->velicina; i++) {
		if (Tab->NizCvorova[i] != NULL) {
			temp = Tab->NizCvorova[i];
			next = temp;
			while (next != NULL) {
				next = temp->next;
				free(temp);
				temp = next;
			}
			Tab->NizCvorova[i] = NULL;
		}
	}
	return EXIT_SUCCESS;
}