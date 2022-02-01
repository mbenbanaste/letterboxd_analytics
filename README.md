# letterboxd_analytics

I'm working on an analytics service that provides more data than the website's paid service provides. 
For example, I'd like to see not just who are the top 25 directors whose films I watch the most (or those films I rate highest), but perhaps top X number of directors whose films I watched the most in 70s (or any year or decade); likewise, perhaps I'd like to know which directors (or actors/actresses) from Korea, i.e., films produced in Korea, I rate the highest and such more layered information. 

*** Work in progress ***

I'd like to add a recommendation system as well based on one's watch history and preferences, and I do have several models, but none satisfy me enough currently so I keep on working on them.
The main problem, besides that even one or two thousand watched films do not constitute a large enough dataset, which is high for a regular user, is the complexity, e.g. too many outliers in various kinds, and the number of the variables at hand.
Also, if we turn all variables to numerical or categorical values, information I'd like to incorporate in the system gets lost; specifically, I'd like to include a film's description in the system in addition to information on actors, year produced, genre and such more categorizable data.
The solution, ideally, would be to transform all variables, including the description, into a single variables, i.e. a paragraph.
For example, for any film, the variable would be, roughly, "The name of the film is [name]. It's director is [director]. It is about [description]...,' which would then be processed via, for example, BERT.
