clc
clear
close all
 %% World Happiness Ranking (optimierter Import)
WHR_file = "WHR25_Data_Figure_2.1v3.xlsx";

% Einlesen OHNE Änderung der Spaltennamen!
T_WHR = readtable(WHR_file, ...
                  "TextType", "string", ...
                  "VariableNamingRule", "preserve");


%% --- Spaltennamen prüfen ---
% (zeigt dir die echten Spaltennamen aus der Datei)
disp(T_WHR.Properties.VariableNames')


%% --- Spaltennamen korrekt zuweisen ---
% Liste der alten und neuen Spaltennamen
oldNames = {...
    'Country name', ...
    'Happiness rank', ...
    'Life evaluation (3-year average)', ...
    'Lower whisker', ...
    'Upper whisker', ...
    'Explained by: Log GDP per capita', ...
    'Explained by: Social support', ...
    'Explained by: Healthy life expectancy', ...
    'Explained by: Freedom to make life choices', ...
    'Explained by: Generosity', ...
    'Explained by: Perceptions of corruption', ...
    'Dystopia + residual'};

newNames = {...
    'CountryName', ...
    'Rank', ...
    'LifeEvaluation', ...
    'LowerWhisker', ...
    'UpperWhisker', ...
    'LogGDP', ...
    'SocialSupport', ...
    'HealthyLifeExpectancy', ...
    'Freedom', ...
    'Generosity', ...
    'PerceptionsOfCorruption', ...
    'DystopiaResidual'};

% Schleife zum Umbenennen der Spalten
for k = 1:length(oldNames)
    idx = strcmp(T_WHR.Properties.VariableNames, oldNames{k});
    if any(idx)
        T_WHR.Properties.VariableNames{idx} = newNames{k};
    end
end



%% Beispiel: Deutschland – WHR plotten (optimiert)

% Datentypen für wichtige Spalten festlegen
T_WHR.CountryName = string(T_WHR.CountryName);
T_WHR.Year = double(T_WHR.Year);
T_WHR.Rank = double(T_WHR.Rank);

% Deutschland-Daten herausfiltern
T_DE = T_WHR(T_WHR.CountryName == "Germany", :);

% Nach Jahr sortieren
T_DE = sortrows(T_DE, "Year");

T_DE.Year = double(T_DE.Year);
T_DE.Rank = double(T_DE.Rank);

% Mittelwert Ranking Deutschland
middleRanking = mean(T_DE.Rank);
disp(middleRanking);

% Linienplot
figure
plot(T_DE.Year, T_DE.Rank, "-o", "LineWidth", 2, "MarkerSize", 6)
set(gca, "YDir", "reverse")   % Rank 1 oben
xlabel("Jahr")
ylabel("Happiness Rank")
title("World Happiness Ranking – Germany")
grid on

% Barplot
figure
bar(T_DE.Year, T_DE.Rank)      % barplot → bar()
set(gca, "YDir", "reverse")    % Rank 1 oben
xlabel("Jahr")
ylabel("Happiness Rank")
title("World Happiness Ranking – Germany (Barplot)")
grid on
