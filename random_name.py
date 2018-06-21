import random

import os

import model

FIRST_MALE = ['Abraham', 'Adam', 'Adi', 'Adina', 'Adir', 'Agam', 'Aharon', 'Akiba', 'Akiva', 'Almog', 'Alon', 'Amichai',
              'Amir', 'Amit', 'Amnon', 'Amos', 'Anan', 'Anat', 'Ari', 'Arie', 'Arieh', 'Ariel', 'Arik', 'Aryeh', 'Asa',
              'Asaf', 'Asher', 'Avi', 'Avidan', 'Avihu', 'Aviram', 'Avishai', 'Aviv', 'Aviya', 'Avner', 'Avraham',
              'Avram', 'Ayal', 'Barak', 'Baruch', 'Barukh', 'Binyamin', 'Boaz', 'Chaim', 'Chayim', 'Chayyim', 'Chen',
              'Chesed', 'Dan',
              'Daniel', 'Dar', 'David', 'Dekel', 'Deror', 'Dikla', 'Diklah', 'Dor', 'Dori', 'Doron', 'Dov', 'Dror',
              'Eden',
              'Efraim', 'Ehud', 'Eiran', 'Eitan', 'Elah', 'Elazar', 'Eli', 'Eli', 'Eliezer', 'Elijah', 'Elior',
              'Eliyahu',
              'Eliyyahu', 'Elkan', 'Ephraim', 'Erez', 'Eyal', 'Eytan', 'Ezra', 'Gal', 'Gavriel', 'Gideon', "Gid'on",
              'Gil',
              'Gilad', 'Gili', 'Hadar', 'Haim', 'Harel', 'Hayim', 'Hayyim', 'Hebel', 'Hed', 'Hevel', 'Hillel', 'Hyam',
              'Idan', 'Ilan', 'Immanuel', 'Ira', 'Itai', 'Itamar', 'Itzhak', 'Iyov', 'Jaffe', 'Jaron', 'Keshet', 'Kfir',
              'Lavi', 'Lev', 'Levi', 'Li', 'Lior', 'Liron', 'Maayan', 'Malachi', 'Maor', 'Matan', 'Mattityahu', 'Meir',
              'Melech', 'Melek', 'Menachem', 'Menahem', 'Menashe', 'Meshulam', 'Meshullam', 'Meyer', "Mikha'el",
              'Miron',
              'Mor', 'Moran', 'Mordecai', 'Mordechai', 'Moshe', 'Nachum', 'Nadav', 'Natan', 'Nathan', 'Nir', 'Nitzan',
              'Niv',
              'Noach', 'Noam', 'Noga', 'Nogah', 'Noy', 'Ofek', 'Ofer', 'Ofir', 'Ofra', 'Omer', 'Omri', 'Or', 'Orel',
              'Oren',
              'Ori', 'Osher', 'Ovadia', 'Oved', 'Oz', 'Paz', 'Peleg', 'Peretz', 'Pinchas', 'Raanan', 'Ravid', 'Raz',
              'Reuben', 'Reuven', 'Roi', 'Ron', 'Ronen', 'Rotem', 'Sagi', 'Shachar', 'Shahar', 'Shai', 'Shaked',
              'Shalev',
              'Shalom', 'Shani', 'Shaul', 'Shay', 'Shimon', 'Shimshon', 'Shlomo', 'Shmuel', 'Simcha', 'Stav', 'Tal',
              'Tam',
              'Tamir', 'Tom', 'Tomer', 'Tovia', 'Tuvya', 'Tzafrir', 'Tzion', 'Tzvi', 'Udi', 'Uri', 'Uriel', 'Uzi',
              'Uzzi',
              'Uzziel', 'Yaakov', 'Yachin', 'Yafe', 'Yaffe', 'Yair', 'Yakov', 'Yaniv', 'Yarden', 'Yaron', 'Yechezkel',
              'Yehiel', 'Yehonatan']

FIRST_FEMALE = ['Achinoam', 'Adara', 'Adena', 'Adi', 'Adina', 'Adva', 'Agam', 'Ahava', 'Ahuva', 'Aliya', 'Aliyah',
                'Aliza', 'Alma', 'Almog', 'Alona', 'Amira', 'Amit', 'Anat', 'Ariel', 'Atalia', 'Atara', 'Atarah',
                'Avia', 'Avigail', 'Avishag', 'Aviv', 'Aviva', 'Aviya', 'Ayala', 'Ayelet', 'Ayla', 'Bashe', 'Basia',
                'Basya', 'Batel', 'Batsheva', 'Batya', 'Batyah', 'Beracha', 'Bosmat', 'Bracha', 'Chanah', 'Channah',
                'Chava', 'Chaya', 'Chen', 'Chesed', 'Dafna', 'Dalia', 'Dalit', 'Dalya', 'Dana', 'Danya', 'Dar',
                'Deborah', 'Derorit', 'Devorah', 'Dikla', 'Diklah', 'Dor', 'Dorit', 'Drorit', 'Dvorah', 'Eden', 'Efrat',
                'Elah', 'Eliana', 'Eliora', 'Elisheva', 'Elke', 'Gal', 'Galia', 'Galit', 'Geula', 'Gilah', 'Gili',
                'Hadar', 'Hadas', 'Hadassah', 'Hagit', 'Hannah', 'Hava', 'Hed', 'Herut', 'Hila', 'Ilana', 'Ilanit',
                'Inbal', 'Inbar', 'Irit', 'Jaffe', 'Kelila', 'Keren', 'Keshet', 'Kineret', 'Kinneret', 'Leah', 'Li',
                'Liat', 'Libi', 'Lihi', 'Lilach', 'Lior', 'Liora', 'Liorit', 'Liron', 'Lital', 'Livna', 'Livnat',
                'Maayan', 'Malka', 'Margalit', 'Margalita', 'Marganita', 'Maya', 'Maytal', 'Meira', 'Meirit', 'Meital',
                'Menuha', 'Merav', 'Michal', 'Miriam', 'Mor', 'Moran', 'Naamah', 'Nahal', 'Naomi', 'Nava', 'Nessa',
                'Neta', 'Netta', 'Nili', 'Nissa', 'Nitza', 'Nitzan', 'Noa', 'Noam', 'Noga', 'Nogah', 'Noy', 'Noya',
                'Nurit', 'Odelia', 'Ofir', 'Ofira', 'Ofra', 'Or', 'Ora', 'Orah', 'Ori', 'Orit', 'Orli', 'Orly', 'Orna',
                'Paz', 'Rachel', 'Rani', 'Ravid', 'Raz', 'Raziela', 'Reut', 'Rina', 'Rinat', 'Riva', 'Rivka', 'Ron',
                'Rona', 'Roni', 'Ronit', 'Rotem', 'Rut', 'Sagit', 'Sapir', 'Sarah', 'Sarit', 'Shachar', 'Shahar',
                'Shaked', 'Shalev', 'Shamira', 'Shani', 'Shay', 'Shifra', 'Shir', 'Shira', 'Shiri', 'Shirli', 'Shlomit',
                'Shoshana', 'Shoshannah', 'Shulamit', 'Shulamith', 'Shulammit', 'Shulammite', 'Sigal', 'Sigalit',
                'Simcha', 'Smadar', 'Stav', 'Tal', 'Tali', 'Talia', 'Talya', 'Tam', 'Tamar', 'Tehila', 'Tikva',
                'Tirtzah', 'Tom', 'Tova', 'Tovah', 'Tovia', 'Tsila', 'Tzila', 'Tzipora', 'Tziporah', 'Tzipporah',
                'Tzivia', 'Tzivya', 'Tzofiya', 'Tzufit', 'Tzvia', 'Varda', 'Vardah', 'Vered', 'Yaara', 'Yachna', 'Yael',
                'Yaen']

FAMILY = ['Zeisig', 'Gnademann', 'Goldshine', 'Gerlitz', 'Salzkotter', 'Hirschbock', 'Vlcker', 'Besselsohn',
          'Schlusselberg', 'Persikaner', 'Kaas', 'Gaensler', 'Wiseman', 'Lorieson', 'Marcusius', 'Joseph', 'Schoenhaus',
          'Fisher', 'Ellerich', 'Karewski', 'Guldenberg', 'Engelbert', 'Wittelshofen', 'Schamburger', 'Juetel',
          'Herbes', 'Poorten', 'Dobrin', 'Haagen', 'Butschatscher', 'Mosenthal', 'Tachauer', 'Katzer', 'Liebschuetzer',
          'Sachsel', 'Nadig', 'Rieberger', 'Pommer', 'Alsfeld', 'Creizenach', 'Uffenheimer', 'Goltmann',
          'Pyzdrskiquack', 'Allersheimer', 'Mhlstein', 'Briel', 'Homburger', 'Zgall', 'Steinhaender', 'Stadtmller',
          'Eibeschuetz', 'Erdheim', 'Jakubinski', 'Kopp', 'Bendick', 'Manteuffel', 'Wildberger', 'Arnthal',
          'Sonnenfield', 'Spanjer', 'Hummel', 'Schuffter', 'Rastaetter', 'Altkirch', 'Bo', 'Quadros', 'Krepsig',
          'Schnerb', 'Tworoger', 'Schfer', 'Klaar', 'Koppler', 'Fachtan', 'Rotenberg', 'Dhrenheimer', 'Biegard',
          'Wertheimstein', 'Gruenenthal', 'Angres', 'Zuerndorfer', 'Bischofsheimer', 'Bodenthal', 'Waldenberg',
          'Froehlichstein', 'Kronfeld', 'Shoyer', 'Benas', 'Neuhann', 'Derkheim', 'Bischoffsheim', 'von', 'Zenner',
          'Kracauer', 'Petschel', 'Mairhofer', 'Falklein', 'Katz', 'Corschmann', 'Wirsching', 'Schneidinger', 'Deiches',
          'Japhet', 'Lepehn', 'Fallein', 'Brachmann', 'Rosenberger', 'Bath', 'Waldstatt', 'Joachimsen', 'Jacobson',
          'Bruer', 'Baumert', 'Frommer', 'Wendel', 'Starik', 'Beiersdorff', 'Brunnhild', 'Riemon', 'Kanitzer',
          'Auksburg', 'Spangenberg', 'Leipheimer', 'Gurau', 'Chronik', 'Stammfort', 'Ballo', 'Mndlein', 'Rothensss',
          'Franses', 'Stricker', 'Lemnicke', 'Exin', 'Lsser', 'Herrnsheim', 'Eichhold', 'Langguth', 'Szachtel',
          'Settegast', 'Hilbert', 'Lagro', 'Edersheimer', 'Smolinski', 'Weberberg', 'Dosmar', 'Rebstock', 'Zippert',
          'Greiling', 'Friedemann', 'Wolpert', 'Tieber', 'Freudel', 'Leveque', 'Schrader', 'Segan', 'Roberg',
          'Birkenstaedt', 'Ellord', 'di', 'Kaczer', 'Abengaly', 'Dattelfeld', 'Silten', 'Oliveira', 'Ismar',
          'Seyferheld', 'Miodowski', 'Bornheimer', 'Stephanus', 'Kirchstein', 'Chalfan', 'Baernstein', 'Castro',
          'Raybach', 'Dachgruber', 'Buckheimer', 'Ezechel', 'Bendheimer', 'Bellerstein', 'Eifeler', 'Kleineibst',
          'Hirschkowitz', 'Martinez', 'Karfunkelstein', 'Dombrowka', 'Henisch', 'Gruenbaum', 'Etlinger', 'Schramm',
          'Barthmann', 'Wissbader', 'Morreau', 'Bacherach', 'Wiesner', 'Landshoff', 'Sicherer', 'Brisch', 'Steinam',
          'Festenberger', 'Abrahamowski', 'Italiaander', 'Gettenbach', 'Harburger', 'Dinkelsbiel', 'Wirtenberg',
          'Bernstadt', 'Hornemann', 'Susholz', 'Wildeganz', 'Pan', 'Lehmannbeer', 'Wolfreim', 'Alexy', 'Hpner',
          'Merzbach', 'Salzburg', 'Kremer', 'Manhalt', 'Reichlesser', 'Pinkson', 'Lang', 'Einstdter', 'Scherk',
          'Feilchenfeld', 'Behrenheim', 'Gensbourger', 'Schimek', 'Pesach', 'Lapp', 'Schivelbein', 'Spintel',
          'Waitzfelder', 'Heynsen', 'Leerer', 'Menk', 'Krohner', 'Schmolkol', 'Pulver', 'Heinsfurter', 'Lewisson',
          'Coschmann', 'Labandter', 'Rochotss', 'Ganzmann', 'Katscher', 'Michelfeld', 'Wolffsheim', 'Lowenthal',
          'Heiliger', 'Kunreuther', 'Schtz', 'de', 'Meineck', 'Schmuckler', 'Pollak', 'Jesselson', 'Heipert', 'Gollanz',
          'Lindenburg', 'Bech', 'Leron', 'Hony', 'Ochsestern', 'Neustdel', 'Kaliske', 'Cartheuser', 'Barm',
          'Seidenberger', 'Raabe', 'Ensel', 'Westphaeling', 'Bressburger', 'Gerhard', 'Libschtz', 'Frohlichstine',
          'Josephin', 'Eschwe', 'Gue', 'von', 'Volhard', 'Casperson', 'Marona', 'Bcker', 'Ansel', 'Muthart',
          'Andressen', 'Pyrschenk', 'Liepold', 'Birgheim', 'Althauser', 'Gollanscher', 'Poper', 'Brummet', 'Stopek',
          'Brle', 'Dobrien', 'der', 'Bissinger', 'Karbach', 'Schilling', 'Linauer', 'Arenhold', 'Samst', 'Ballhorn',
          'Schlesien', 'Bayerthal', 'Einsiedler', 'Dillow', 'Gundersheim', 'Bieler', 'Tiras', 'Schneidacher',
          'Strehlitz', 'Waescher', 'Grunebaldt', 'Andrade', 'Somann', 'Spiro', 'Haindorff', 'Morgenroth', 'Samstag',
          'Weich', 'Pfeiffer', 'Moschkowski', 'Ploetzki', 'Valffer', 'Lippochowitz', 'Belgard', 'Kandler', 'Glitz',
          'Wickart', 'Schmaje', 'Danckwerth', 'Cann', 'Bergthal', 'Burgass', 'Jahnsen', 'Reh', 'Jalowicz', 'Hausner',
          'Hopfmann', 'Schies', 'Rischar', 'Flrscheim', 'Blumenau', 'Berlak', 'Nol', 'Cirulnik', 'Simundt', 'Schchter',
          'Mertzbacher', 'Elzas', 'Lesser', 'Hoeppner', 'Lismann', 'Daust', 'Eichengruen', 'Schrage', 'Voos',
          'Krotoski', 'Caspery', 'Rottmilch', 'Tschierske', 'Perlchen', 'Deffson', 'Seckelmann', 'Weisbart', 'Xidz',
          'Livaux', 'Bielfeld', 'Walston', 'Algasi', 'Hesdoerffer', 'van', 'Marx', 'Mondschein', 'Schlochau',
          'Warschau', 'Ringlein', 'Loth', 'Warisch', 'Hoefler', 'Deinhauser', 'Gdemann', 'Lauder', 'Rassner', 'Zappart',
          'Mhlhaeusser', 'Schnig', 'Baad', 'Colman', 'Dachsteiner', 'Wahrmund', 'Andrea', 'Reuling', 'Klauss', 'Magner',
          'Poremsky', 'Ettenheimer', 'Ettig', 'Cronach', 'Berwein', 'Jeitteles', 'Isenthal', 'Dzaliner', 'Wrdenberger',
          'Fite', 'Weiswachs', 'Steinsberger', 'Walzer', 'Jakobowski', 'Futtergaarde', 'Felklein', 'Mendersohn',
          'Baerlach', 'Berlatsch', 'Werner', 'Pass', 'Rathmann', 'Schnellenburg', 'Fluersheim', 'Michlsohn',
          'Carlibach', 'Tppel', 'Goldschild', 'Hockstadter', 'de', 'Disbeck', 'Koronna', 'Nordhuser', 'Carcasona',
          'Jakolz', 'Halm', 'Goldschmiet', 'Hill', 'Sassmann', 'Baginsky', 'Cannstadt', 'Eliston', 'Cowitz', 'Kemper',
          'Fiktin', 'Lichtensttter', 'Blumgard', 'Lwenberger', 'Holz', 'Salzmann', 'Schlch', 'Medeira', 'Zifi', 'Baum',
          'Liefges', 'Placzek', 'Issmar', 'de', 'Berwanger', 'Bak', 'Menge', 'Utitz', 'Andre', 'Meinfelder', 'Lobred',
          'Scheye', 'Bernheimb', 'Rimini', 'Ungar', 'Oberdoerfer', 'Hutemann', 'Frankenauer', 'Jeroslaw', 'Krakau',
          'Schwalheimer', 'Lanzberg', 'Daiges', 'Konstadt', 'Willstaetter', 'Boskowitz', 'Hoechheimer', 'Marienthal',
          'Wirzburg', 'Dessauer', 'Binnek', 'Eichengreen', 'Tobe', 'Aronbach', 'Resener', 'Langgaesser', 'Merlnder',
          'Rochmann', 'Goetzel', 'Lies', 'Greenfield', 'Goldfrank', 'Meerapfel', 'Rain', 'Frankenschwerth',
          'Schiffmann', 'Ladendorf', 'Lwenbaum', 'Gewinner', 'Manhald', 'Gemnd', 'Sterner', 'Maynthal', 'Hetzer',
          'Mattos', 'Gottheil', 'Bassfreund', 'Weinreb', 'Cosler', 'Ruff', 'Helbronner', 'Meimberg', 'Erlbacher',
          'Rossheimer', 'Mosenthal', 'Erbsfeld', 'Kindermann', 'Bitiner', 'Eisack', 'Bruch', 'Nossen', 'Hardy',
          'Wahlheimer', 'Immerfroh', 'Hoxter', 'Kraus', 'Rottweiler', 'Brezinski', 'Bechhoff', 'Fassbender',
          'Pflaumloch', 'Chraplewsky', 'Oliva', 'Waldenberger', 'Tuch', 'Zwirn', 'Schoenflies', 'Giefenow', 'Elkusch',
          'Ekstein', 'Mossler', 'Brilin', 'Schoolherr', 'Essig', 'Nelke', 'dayola', 'Mortgen', 'Gemeiner', 'Dinkelman',
          'Ahrend', 'May', 'Meerlaender', 'Beradt', 'Sobotka', 'Becher', 'Lychenhain', 'Heymannrosenstamm', 'Meppelt',
          'Burgunder', 'Clausdorf', 'Tischmann', 'Benzbach', 'Sgall', 'Lvison', 'Ahrons', 'Matzdorfer', 'Dorschfeld',
          'Frschheimer', 'Model', 'Grodzensky', 'Helbert', 'Traut', 'Norlaender', 'Boschewitz', 'Tillian', 'Lewinsky',
          'Chotzem', 'Mhringer', 'Lassar', 'Seilberger', 'Grllinger', 'Samoscz', 'Bding', 'Pragheim', 'Mikolasch',
          'Wartenburg', 'Jablonski', 'Passarinho', 'Rintelsohn', 'Kleissner', 'Adelstein', 'Monath', 'Kammerberger',
          'Lffler', 'Dessau', 'Brokema', 'Elsberg', 'Pelz', 'Hirschbaum', 'Niello', 'Berne', 'Potzernheim', 'Meister',
          'Viebeck', 'Gomo', 'Elsaesser', 'Hell', 'Bartholdi', 'Heimberger', 'Stockheim', 'Bajon', 'Ehrenfest',
          'Roedelmeyer', 'Vassen', 'dazevedo', 'Dias', 'Schreuer', 'der', 'Kantor', 'Beyl', 'Goldstein', 'Czarny',
          'Vitt', 'Voreiter', 'Mejrowski', 'Bildstein', 'Bien', 'Kiez', 'Weldt', 'Curiel', 'Baehrendt', 'Bresinski',
          'Feinmann', 'Hallerstein', 'Kohler', 'Hinrichsen', 'Moro', 'Apstein', 'Groshut', 'Sssbach', 'Lui',
          'Sonnengard', 'Reschower', 'Popower', 'Gensler', 'Schwartzheim', 'Wasmuth', 'Grlitz', 'Fleisch', 'Falkenburg',
          'Lemos', 'Pilitzer', 'Schaack', 'Goldkette', 'Levy', 'Unna', 'Laurenz', 'Wahr', 'Durbacher', 'Sintzheimer',
          'Baywood', 'Gumbel', 'Aussee', 'Heinersdorf', 'Fabian', 'Tikotin', 'Friesenhaeuser', 'Orgler', 'Dalsimer',
          'Klocke', 'Elimeyer', 'Vogelstein', 'Egenhuser', 'Brhn', 'Horkheimer', 'Westerburger', 'Bok', 'Hammelfett',
          'Haarzopf', 'Schwirklanski', 'Ordenstein', 'Yseckel', 'Ludomer', 'Wahrendorf', 'Mandel', 'Strck', 'Groe',
          'Kmmelstiel', 'Lebenheim', 'Wagenheimer', 'Hoffmann', 'Helper', 'Benario', 'Simonetti', 'Leibig', 'Frommholz',
          'Trenkel', 'Rathheim', 'Woeller', 'Frommelt', 'Marces', 'Rodenfels', 'Hilpoltsteiner', 'Gosslar', 'Hantke',
          'Merziger', 'Wilczynski', 'Reismann', 'Maarssen', 'Glasfeld', 'Vogts', 'Pfann', 'Legout', 'Eliassohn',
          'Heydweyer', 'Martienssen', 'Kurlnder', 'Roescher', 'Mehringen', 'Freundlich', 'Kaunitz', 'Saft',
          'Eisenmann', 'Ssel', 'Azevedo', 'Glauberg', 'Turbin', 'Andresen', 'Zadig', 'Falken', 'Mundt', 'Kronenberg',
          'Leibhold', 'Kaspar', 'Spanjerherford', 'Hamletter', 'Groschler', 'Murtmann', 'Ruhm', 'Hoenle', 'Isaacs',
          'Brnitzer', 'Re', 'Wulffs', 'Bruecker', 'Albertsweiler', 'Luettke', 'Brinck', 'Klopstock', 'Selkes',
          'Blochmock', 'Kratzik', 'Calenberg', 'Heydegger', 'Magnus', 'Lissauer', 'Gundersblum', 'Guettermann', 'Rina',
          'Zopp', 'Ahronheim', 'Gugenheim', 'Weihl', 'Adelsberger', 'Samulon', 'Schps', 'Bodky', 'Weinland', 'Krein',
          'Dio', 'Wollheim', 'Fuerstenwalde', 'Richardt', 'Waldow', 'Welauer', 'Wronker', 'Bilawski', 'Rotthaus',
          'Teckler', 'Tannenwald', 'Hartstein', 'Nathanschin', 'Weinhouse', 'Lebbin', 'Kyack', 'Atias', 'Delmedigo',
          'Wimpelberg', 'Nuez', 'Stuler', 'Goldsohn', 'Melwing', 'Naeter', 'Sahlke', 'Sigalla', 'Waxmann', 'Baden',
          'ttinger', 'Steinbacher', 'Kurzewski', 'Allerberg', 'Oberfelder', 'Pilz', 'Steiner', 'Wrttemberg',
          'Ollendorff', 'Falkner', 'Goschtzer', 'Herscher', 'Traenkel', 'Mever', 'Astruk', 'Guensburg', 'Kallir',
          'Lilienfeldt', 'Schalle', 'Graber', 'Ritzwoller', 'Wing', 'Steingsser', 'Engel', 'Korda', 'Moderze', 'Smann',
          'Jachmann', 'Gnsburger', 'Gritz', 'Newhofer', 'Hhnlein', 'Nehlhaus', 'Ssholz', 'Lambert', 'Mndel',
          'Flahinger', 'Michelsen', 'Brikheimer', 'Kunreiter', 'Windecken', 'Hthmann', 'Angerthal', 'Biale', 'Brillin',
          'Morro', 'Eckmann', 'Margoliner', 'Wacher', 'Fromm', 'Dmann', 'Volks', 'Schiksal', 'Spiesberger', 'Haymann',
          'Gademann', 'Antones', 'Zielinsky', 'Dossenheim', 'Shaltiel', 'Rinteln', 'Wolfgramm', 'Herzhorn', 'van',
          'Bue', 'Scholim', 'Hollaender', 'Kochloeffel', 'Kurtenbach', 'Reece', 'Peyser', 'Seelberg', 'Hollenstein',
          'Dorum', 'Teomim', 'Warendorff', 'Jarotschinski', 'Weisenheimer', 'Leitner', 'Klefmann', 'Kapell',
          'Juliusberger', 'Soberski', 'Fchtenberg', 'Freitel', 'Maron', 'Bock', 'Altbayer', 'Burggraf',
          'Cassuto', 'Merk', 'Wachmann', 'Schiela', 'Beiersdorfer', 'Laudenheimer', 'Bttinger', 'Toltz',
          'Slotowe', 'Wernthal', 'Segnitz', 'Monkewitz', 'Simons', 'Seeheim', 'Heimbach', 'Juenger', 'Lwen', 'Sintz',
          'Greiditz', 'Chrzelitz', 'Haindorf', 'Natorff', 'Salfeld', 'Perls', 'Meinfeld', 'Bonum', 'Weitzenfelder',
          'Spahn', 'Brentano', 'Beith', 'Weisweiller', 'Diespecker', 'Wagenbauer', 'Hffer', 'Schwanfelder', 'Grhn',
          'Joel', 'Buchenfeld', 'Hirschberger', 'Merck', 'Pinkerle', 'Debrich', 'Nther', 'Mosenhauer', 'Schliwinsky',
          'Gerathwohl', 'Lowenburg', 'Kirk', 'Hirschelsohn', 'Horchheimer', 'Gundolf', 'Wohlmann', 'Sakutscher',
          'Skutset', 'Dtelbach', 'Umstdter', 'Schoenmueller', 'Bluhm', 'Buchheim', 'Boeheimer', 'Machuel',
          'Schwerinsky', 'Theisebach', 'Harmelin', 'Freiburger', 'Frieslaender', 'Spigel', 'Goschtz', 'Koenigswarter',
          'Leluw', 'Noherr', 'Brumet', 'Bottiwies', 'Bechhofen', 'Handtke', 'Krainski', 'Wulfsohn', 'Kanheimer',
          'Ilbesheim', 'Renard', 'Sust', 'Lessing', 'Teble', 'Pinkussohn', 'Skubich', 'Goltschmidt', 'Loe', 'Neuwerth',
          'Robinson', 'Mr', 'Raczynski', 'Obersitzki', 'Huth', 'Stierstdter', 'Kreissdorfer', 'Monschke', 'Eilnder',
          'Solemeel', 'Salba', 'Khne', 'Nowra', 'Kallmes', 'Steinweg', 'Hartung', 'Wolfstein', 'Lavian', 'Frankenlnder',
          'Lahr', 'Polley']


def generate_name(male):
    return '{} {}'.format(random.choice(FIRST_MALE if male else FIRST_FEMALE), random.choice(FAMILY))


def generate_pic(male):
    pics_dir = os.path.join(model.IMAGE_DIR, 'profile', 'male' if male else 'female')
    return os.path.join(pics_dir, random.choice(os.listdir(pics_dir)))


if __name__ == '__main__':
    print(generate_name(False))
    print(generate_name(True))
