video-tags-suggestion
=====================

This project aims to suggest tags based on video metadata. It has 3 steps:

STEP 1
------
### Store/update a database with the total of tags related to a term.

	- Example: term = neymar

	TERM:NEYMAR
		SANTOS: 100
		FUTEBOL: 80
		DANCINHA: 10
	TERM:NEYMAR:COUNT 190

	It means that there's 100 videos with NEYMAR in its title or description
	and SANTOS as one tag. The same for FUTEBOL tag, where it is presented in
	80 videos that has NEYMAR in its title or description.

STEP 2
------
### Calculates the proportion of each tag related to a term

	TERM:NEYMAR:PROPORTIONS
		SANTOS: 0.5263157894736842
		FUTEBOL: 0.42105263157894735
		DANCINHA: 0.05263157894736842

	- This data should be fetched through an API:
		GET POPULAR/neymar

		{
		    term: "neymar",
		    tags: {
			"SANTOS": 0.5263157894736842,
			"FUTEBOL": 0.42105263157894735,
			"DANCINHA": 0.05263157894736842
		    }
		}

Both steps are done as jobs. The third step is the real interface of the system.

STEP 3
------
### Receive a text (title + description), tokenize/analyse it and use the API above
to fetch their most used tags and proportions. Then, all tags fetched are
merged into one array of sorted tags and return the 3 heaviest tags.

	- Example: Neymar faz 3 gols

	1) Analyzed text: Neymar gols
	2) From Neymar:
		{
			"santos": 0.5263157894736842,
			"futebol": 0.42105263157894735,
			"dancinha": 0.05263157894736842
		}
	From gols:
		{
			"futebol": 0.9,
			"santos": 0.000001,
			"fluminense": 0.004
		}
	Merged:
		{
			"futebol": 1.32105263157894735,
			"santos":  0.5263167894736842,
			"dancinha": 0.05263157894736842,
			"fluminense": 0.004
		}

Suggested tags: futebol, santos
