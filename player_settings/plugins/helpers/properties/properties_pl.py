# report info

pdf_report_file_name = "raport_pupil_{}.pdf"
report_title = "Analiza danych okulograficznych"
report_subtitle = "Raport z wykresami"
subtitle_with_date = "Data utworzenia: {}"
subtitle_with_rec_dir_path = "Katalog z nagraniem: {}"
subtitle_with_exported_dir_path = "Katalog z wyeksportowanymi danymi: {}"

# subsections
fixation_subsection_title = "Fiksacje"
fixation_subsection_description = \
    "\n      Fiksacje to ruchy, które stabilizują siatkówkę oka, " \
    "aby mógł się na niej (konkretniej: w jej centralnej części, " \
    "czyli plamce żółtej) wytworzyć ostry obraz. W rzeczywistości są one złożeniem " \
    "mikroruchów oka tj. tremoru, mikrosakad oraz dryftu, " \
    "które przyczyniają się do poszerzenia precyzyjnego pola widzenia. " \
    "Fiksacje interpretuje się jako punkty skupienia wzroku " \
    "na konkretnym fragmencie widzialnego obrazu, trwające około 200 - 300 ms." \
    "\n\n      Istnieją różne metody identyfikacji fiksacji i sakad. " \
    "W oprogramowaniu Pupil do ich znalezienia zastosowano algorytm I-DT (ang. Dispersion-Threshold Identification), " \
    "oparty o dyspersję, który posługuje się dwoma parametrami: " \
    "wartością dyspersji oraz czasu trwania fiksacji. " \
    "Metoda ta wykorzystuje fakt, iż punkty fiksacji (ze względu na małą prędkość) " \
    "mają tendencję do występowania blisko siebie. " \
    "Fiksacje identyfikowane są jako grupy kolejnych punktów w ramach ustalonej dyspersji (tj. rozproszenia)."
fixation_detector_table_description = "\n\n      Ustawienia parametrów pluginu Fixation Detector w Pupil Capture oraz " \
                                      "całkowita liczba fiksacji w nagraniu: "
fixation_detector_settings_values_param = "PARAMETR"
fixation_detector_settings_values_val = "WARTOŚĆ"

saccades_subsection_title = "Sakady"
saccades_subsection_description = \
    "\n      Sakada to szybki i gwałtowny ruch skokowy, następujący po każdej fiksacji. " \
    "Tego rodzaju ruchy mają za zadanie przemieścić część środkową plamki żółtej " \
    "(tzw. dołek centralny) do nowej pozycji w polu widzenia. " \
    "Następuje tutaj decyzja mózgu o tym, na jaki element ma być skierowany wzrok, " \
    "czyli gdzie ma nastąpić kolejna fiksacja. Ruchy sakadyczne są zarówno dobrowolne " \
    "jak i bezwarunkowe. Czas trwania sakad wynosi około 10-100 ms, " \
    "natomiast ich prędkość może osiągnąć nawet 500 stopni kątowych na sekundę."

not_defined_area = "not_on_any_surface"

# descriptions for plots in report

#########################################################
#       Surface visibility
#########################################################

surface_visibility_plot_title = "Widoczność powierzchni"
surface_visibility_percentage_description = \
    "\n      Powyższy wykres pokazuje ile procentowo czasu użytkownik patrzył na " \
    "poszczególne powierzchnie, które zostały zdefiniowane na potrzeby " \
    "badania okulograficznego. Dane eye-trackingowe, na podstawie których " \
    "wykres został stworzony, zostały zaczerpnięte z pliku o nazwie " \
    "\"surface_gaze_distribution.csv\", w którym znajdują się informacje o " \
    "liczbie tzw. \"punktów spojrzeń\" (ang. \"gaze_points\") na poszczególnych " \
    "powierzchniach, a także o całkowitej liczbie tych punktów w kontekście " \
    "całego nagrania (wartość parametru \"total_gaze_point_count\")."
surface_visibility_percentage_filename = "surface_visibility_percentage.png"  # image file (i.e. plot, chart or diagram)

#########################################################
#       Fixations per surface
#########################################################

fixations_count_per_surface_plot_title = "Fiksacje na powierzchniach"
fixations_count_per_surface_description = \
    "      Wykres pokazuje liczbę oraz czas trwania fiksacji " \
    "zarejestrowanych na zdefiniowanych powierzchniach. " \
    "Do wygenerowania tego wykresu posłużono się danymi w " \
    "plikach z prefiksem \"fixations_on_surface\", które zawierają informacje o " \
    "parametrach takich jak: " \
    "\n- id (numer identyfikacyjny fiksacji)" \
    "\n- start_timestamp (początek fiksacji)" \
    "\n- duration (czas trwania fiksacji [ms])" \
    "\n- on_srf (parametr wskazujący czy fiksacja była na danej powierzchni) " \
    "\nUWAGA: Uwzględniono tu wyłącznie fiksacje z wartością parametru \"on_srf\" " \
    "równą True. W niektórych przypadkach wartość tego parametru jest prawdziwa " \
    "dla 2 powierzchni jednocześnie, dlatego mogą pojawić się rozbieżności " \
    "w wyliczonej tu całkowitej liczbie fiksacji."
fixations_count_per_surface_filename = "fixations_count_per_surface.png"

#########################################################
#       Fixations frequency
#########################################################

fixations_frequency_plot_title = "Częstotliwość fiksacji"
fixations_frequency_description = \
    "\n      Wykres przedstawia częstotliwości fiksacji na poszczególnych powierzchniach. " \
    "Średnia częstotliwość to iloraz całkowitej liczby fiksacji " \
    "i czasu trwania całego nagrania, natomiast częstotliwość fiksacji " \
    "na konkretnej powierzchni została obliczona analogicznie, " \
    "jako iloraz liczby fiksacji na danej powierzchni oraz " \
    "czasu wpatrywania się w tą powierzchnię." \
    "\nDo stworzenia powyższego wykresu posłużono się danymi " \
    "w pliku \"surface_gaze_distribution.csv\" oraz w plikach " \
    "z prefiksem \"fixations_on_surface\"."
fixations_frequency_filename = "fixations_frequency.png"

#########################################################
#       Fixations durations
#########################################################

fixations_durations_plot_title = "Fiksacje na osi czasu"
fixations_durations_description = \
    "\n      Wykres obrazuje czasowy rozkład fiksacji. Dane, na podstawie których wygenerowano ten wykres, " \
    "znajdują się w pliku \"info.csv\" oraz w plikach z prefiksem  \"fixations_on_surface\". " \
    "\n\nParametry użyte do obliczeń to m.in.:" \
    "\n- \"start_timestamp\" (czas rozpoczecia każdej fiksacji)," \
    "\n- \"duration\" (długość poszczególnych fiksacji)," \
    "\n- \"Start Time (Synced)\" (czas rozpoczęcia nagrania)," \
    "\n- \"Duration Time\" (długość nagrania)."
fixations_durations_filename = "fixations_durations.png"

#########################################################
#       Saccades count
#########################################################

saccades_count_per_surface_plot_title = "Sakady na powierzchniach"
saccades_count_per_surface_description = \
    "\n      Saccades count - test plot description. Lorem ipsum dolor sit amet, " \
    "sunt in culpa qui officia deserunt mollit anim id est laborum. "
saccades_count_per_surface_filename = "saccades_count_per_surface.png"

#########################################################
#       Heatmaps
#########################################################

heatmaps_plot_title = "Mapy cieplne"
heatmaps_description = \
    "\n      Mapy cieplne stanonwią wizualizację ilości czasu spędzonego na wpatrywaniu się " \
    "w poszczególne obszary na danej powierzchni. Jaśniejsze kolory na mapie oznaczają" \
    "zarejestrowanie wiekszej ilości punktów spojrzeń w danym miejscu, natomiast ciemne regiony mapy to miejsca " \
    "na powierzchni pominięte przez wzrok osoby poddanej badaniu eyetrackingowemu."
heatmaps_filename = "heatmaps.png"

#########################################################
#       Eye movements
#########################################################
eye_movements_title = "Ruchy gałki ocznej"
eye_movements_description = \
    "\n      Istnieje wiele rodzajów ruchów gałki ocznej. W oprogramowaniu Pupil, specjalny plugin " \
    "(Eye Movement Detector) klasyfikuje cztery typy takich ruchów: fiksacje, sakady, post-sakadyczne drgania " \
    "(ang. post-saccadic oscillations, PSO) oraz gładkie podążanie (ang. smooth pursuit)." \
    "\n      Plik \"eye_movement_by_segment.csv\" zawiera dane eyetrackingowe, na podstawie których został " \
    "wygenerowany powyższy wykres. Całkowita liczba fiksacji różni się znacząco w porównaniu do wartości" \
    " podanej w pliku \"fixation_report.csv\", ponieważ w obu pluginach użyte zostały " \
    "różne algorytmy indentyfikujące fiksacje."
eye_movements_filename = "eye_movements_count_and_duration.png"
eye_movements_list = ["fiksacje", "sakady", "PSO", "gładkie podążanie"]

#########################################################
#       plots properties
#########################################################
number_of_movements_label = "Liczba ruchów oka ({})"
number_of_fixations_label = "Liczba fiksacji ({})"
number_of_saccades_label = "Liczba sakad ({})"
movements_durations_axis_label = "Całkowity czas trwania [s]"
fixations_durations_axis_label = "Czas trwania fiksacji [s]"
saccades_durations_axis_label = "Czas trwania sakad [s]"
surface_name_label = "Powierzchnia"
number_of_fixations_per_second_label = "Liczba fiksacji/s"
recording_time_label = "Czas [{}]"
