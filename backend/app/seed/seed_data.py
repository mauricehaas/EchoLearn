import asyncio

from app.core.db import Base, async_session, engine
from app.models.question import Question
from app.models.user import User


async def seed():
    print("Creating tables…")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  # optional, nur für Dev
        await conn.run_sync(Base.metadata.create_all)

    print("Seeding data…")
    async with async_session() as session:
        # Fragen + Antworten
        questions = [
            Question(
                question="Was ist Data Science?",
                answer="Data Science ist ein interdisziplinäres Feld, das wissenschaftliche Methoden, Prozesse, Algorithmen und Systeme verwendet, um Wissen und Erkenntnisse aus Daten zu gewinnen.",
            ),
            Question(
                question="Was sind die wichtigsten Schritte im Data-Science-Prozess?",
                answer="Die wichtigsten Schritte umfassen typischerweise Problemdefinition, Datensammlung, Datenaufbereitung, explorative Datenanalyse, Modellierung, Evaluation und Deployment.",
            ),
            Question(
                question="Was ist der Unterschied zwischen überwachtem und unüberwachtem Lernen?",
                answer="Überwachtes Lernen beinhaltet das Training eines Modells mit gelabelten Daten, wobei der Algorithmus die Beziehung zwischen Eingabefunktionen und Zielvariablen lernt. Unüberwachtes Lernen arbeitet mit ungelabelten Daten und versucht, verborgene Muster oder Strukturen in den Daten zu erkennen.",
            ),
            Question(
                question="Erklären Sie das Bias-Varianz-Dilemma.",
                answer="Das Bias-Varianz-Dilemma ist das Gleichgewicht zwischen dem Fehler, der durch Bias (Underfitting) eingeführt wird, und dem Fehler, der durch Varianz (Overfitting) beim Aufbau eines Machine-Learning-Modells entsteht.",
            ),
            Question(
                question="Was ist Feature Engineering?",
                answer="Feature Engineering ist der Prozess der Auswahl, Transformation und Erstellung von Features aus Rohdaten, um die Modellleistung zu verbessern.",
            ),
            Question(
                question="Wie gehen Sie mit fehlenden Daten in einem Datensatz um?",
                answer="Fehlende Daten können durch Imputationstechniken wie Mittelwert-, Median- oder Modus-Imputation behandelt werden, durch Vorhersagemodelle geschätzt oder durch Löschen von Zeilen oder Spalten mit fehlenden Werten, abhängig von Größe und Art des Datensatzes.",
            ),
            Question(
                question="Was ist Kreuzvalidierung?",
                answer="Kreuzvalidierung ist eine Technik, um die Leistung eines prädiktiven Modells zu bewerten, indem die Daten in mehrere Teilmengen aufgeteilt werden.",
            ),
            Question(
                question="Erklären Sie das Konzept des Overfittings.",
                answer="Overfitting tritt auf, wenn ein Modell die Trainingsdaten zu gut lernt und dabei Rauschen oder zufällige Schwankungen in den Daten anstatt des zugrundeliegenden Musters erfasst.",
            ),
            Question(
                question="Nennen Sie einige gängige Algorithmen für überwachtes Lernen.",
                answer="Gängige Algorithmen umfassen lineare Regression, logistische Regression, Entscheidungsbäume, Random Forests, Support Vector Machines und neuronale Netze.",
            ),
            Question(
                question="Was ist Dimensionsreduktion?",
                answer="Dimensionsreduktion ist der Prozess der Reduzierung der Anzahl von Eingabevariablen in einem Datensatz durch Transformation in einen niedrigdimensionalen Raum unter Erhaltung wichtiger Informationen.",
            ),
            Question(
                question="Was ist Regularisierung im Machine Learning?",
                answer="Regularisierung ist eine Technik, um Overfitting zu verhindern, indem ein Strafterm zur Zielfunktion des Modells hinzugefügt wird.",
            ),
            Question(
                question="Was ist Ensemble-Lernen?",
                answer="Ensemble-Lernen ist eine Technik, die mehrere Machine-Learning-Modelle kombiniert, um Leistung und Robustheit zu verbessern.",
            ),
            Question(
                question="Was ist die ROC-Kurve?",
                answer="Die Receiver Operating Characteristic (ROC)-Kurve ist ein grafisches Diagramm, das die Leistung eines binären Klassifikationsmodells über verschiedene Schwellenwerte hinweg darstellt.",
            ),
            Question(
                question="Was ist AUC-ROC?",
                answer="Die Fläche unter der ROC-Kurve (AUC-ROC) ist eine Metrik zur Bewertung der Leistung eines binären Klassifikationsmodells.",
            ),
            Question(
                question="Was ist der Unterschied zwischen Klassifikation und Regression?",
                answer="Klassifikation ist eine überwachte Lernaufgabe, bei der das Ziel die Vorhersage kategorialer Labels oder Klassen ist, während Regression eine überwachte Lernaufgabe ist, bei der das Ziel die Vorhersage kontinuierlicher numerischer Werte ist.",
            ),
            Question(
                question="Was ist Clustering?",
                answer="Clustering ist eine unüberwachte Lerntechnik, bei der ähnliche Datenpunkte basierend auf ihren Eigenschaften oder Merkmalen gruppiert werden.",
            ),
            Question(
                question="Was ist der Fluch der Dimensionalität?",
                answer="Der Fluch der Dimensionalität bezeichnet das Phänomen, dass die Leistung bestimmter Algorithmen abnimmt, wenn die Anzahl der Features oder Dimensionen in den Daten steigt.",
            ),
            Question(
                question="Was ist der Unterschied zwischen Precision und Recall?",
                answer="Precision misst den Anteil der richtig positiven Vorhersagen unter allen positiven Vorhersagen, während Recall den Anteil der richtig positiven Vorhersagen unter allen tatsächlichen positiven Instanzen misst.",
            ),
            Question(
                question="Was ist der F1-Score?",
                answer="Der F1-Score ist das harmonische Mittel von Precision und Recall und bietet eine einzelne Metrik zur Bewertung der Leistung eines Klassifikators.",
            ),
            Question(
                question="Was ist der Bias eines Schätzers?",
                answer="Der Bias eines Schätzers misst die Differenz zwischen dem erwarteten Wert des Schätzers und dem tatsächlichen Wert des zu schätzenden Parameters.",
            ),
            Question(
                question="Was ist die Varianz eines Schätzers?",
                answer="Die Varianz eines Schätzers misst die Streuung der Schätzerwerte um ihren Erwartungswert.",
            ),
            Question(
                question="Was ist der zentrale Grenzwertsatz?",
                answer="Der zentrale Grenzwertsatz besagt, dass die Stichprobenmittelwertverteilung einer Normalverteilung näherkommt, wenn die Stichprobengröße wächst.",
            ),
            Question(
                question="Was ist Regularisierung in neuronalen Netzen?",
                answer="Regularisierung in neuronalen Netzen beinhaltet das Hinzufügen von Straftermen zur Verlustfunktion, um Overfitting zu verhindern.",
            ),
            Question(
                question="Was ist Batch-Normalisierung?",
                answer="Batch-Normalisierung ist eine Technik in neuronalen Netzen, um die Stabilität und Geschwindigkeit des Trainings durch Normalisierung der Aktivierungen jeder Schicht zu verbessern.",
            ),
            Question(
                question="Was ist Transfer Learning?",
                answer="Transfer Learning ist eine Technik, bei der ein Modell, das auf einer Aufgabe trainiert wurde, als Ausgangspunkt für ein Modell auf einer verwandten Aufgabe wiederverwendet wird.",
            ),
            Question(
                question="Was ist natürliche Sprachverarbeitung (NLP)?",
                answer="NLP ist ein Bereich der künstlichen Intelligenz, der sich mit der Interaktion zwischen Computern und menschlicher Sprache beschäftigt.",
            ),
            Question(
                question="Was sind Wort-Embeddings?",
                answer="Wort-Embeddings sind dichte Vektor-Darstellungen von Wörtern in einem kontinuierlichen Vektorraum.",
            ),
            Question(
                question="Was ist Sentiment-Analyse?",
                answer="Sentiment-Analyse ist eine NLP-Aufgabe, bei der die Stimmung oder Meinung in einem Text identifiziert wird.",
            ),
            Question(
                question="Was ist Deep Learning?",
                answer="Deep Learning ist ein Teilbereich des Machine Learning, der sich auf künstliche neuronale Netze mit mehreren Schichten konzentriert.",
            ),
            Question(
                question="Was ist ein Convolutional Neural Network (CNN)?",
                answer="Ein CNN ist ein neuronales Netz, das besonders gut für strukturierte rasterartige Daten wie Bilder geeignet ist.",
            ),
            Question(
                question="Was ist ein Recurrent Neural Network (RNN)?",
                answer="Ein RNN ist ein neuronales Netz, das sequenzielle Daten verarbeitet und den Zustand vorheriger Eingaben speichert.",
            ),
            Question(
                question="Was ist Reinforcement Learning?",
                answer="Reinforcement Learning ist ein Paradigma, bei dem ein Agent durch Interaktion mit der Umgebung lernt, Entscheidungen zu treffen, um Belohnungen zu maximieren.",
            ),
            Question(
                question="Was ist Q-Learning?",
                answer="Q-Learning ist ein model-freier Reinforcement-Learning-Algorithmus, der die optimale Aktionswahlstrategie für ein Markov-Entscheidungsproblem lernt.",
            ),
            Question(
                question="Was ist der Tradeoff zwischen Exploration und Exploitation?",
                answer="Der Tradeoff beschreibt das Dilemma, ob der Agent neue Aktionen erkunden oder bekannte Aktionen zur Belohnungsmaximierung nutzen sollte.",
            ),
            Question(
                question="Was ist Deep Reinforcement Learning?",
                answer="Deep Reinforcement Learning kombiniert Reinforcement Learning mit Deep Learning, um komplexe Policies direkt aus hochdimensionalen Eingaben zu lernen.",
            ),
            Question(
                question="Was ist ein Markov-Entscheidungsprozess (MDP)?",
                answer="Ein MDP ist ein mathematisches Modell für sequenzielle Entscheidungsfindung, bei dem ein Agent mit einer Umgebung interagiert.",
            ),
            Question(
                question="Was ist Kreuzentropie-Loss?",
                answer="Kreuzentropie-Loss ist eine Verlustfunktion zur Quantifizierung der Differenz zwischen vorhergesagter und tatsächlicher Wahrscheinlichkeitsverteilung in Klassifikationsaufgaben.",
            ),
            Question(
                question="Was ist die Softmax-Funktion?",
                answer="Softmax konvertiert einen Vektor beliebiger reeller Werte in Wahrscheinlichkeiten.",
            ),
            Question(
                question="Was ist der Unterschied zwischen generativen und diskiminativen Modellen?",
                answer="Generative Modelle lernen die gemeinsame Wahrscheinlichkeitsverteilung von Eingabe und Ziel, diskiminative Modelle lernen die bedingte Verteilung des Ziels gegeben der Eingaben.",
            ),
            Question(
                question="Was ist ein Autoencoder?",
                answer="Ein Autoencoder ist ein neuronales Netz, das darauf trainiert wird, seine Eingabedaten am Ausgang wiederherzustellen.",
            ),
            Question(
                question="Was ist der Unterschied zwischen Bagging und Boosting?",
                answer="Bagging erstellt mehrere Modelle unabhängig und kombiniert sie, Boosting erstellt Modelle sequenziell, wobei Gewicht auf Fehlklassifizierungen gelegt wird.",
            ),
            Question(
                question="Was ist Hyperparameter-Tuning?",
                answer="Hyperparameter-Tuning ist der Prozess, optimale Hyperparameter für ein Modell zu finden, um die Leistung zu verbessern.",
            ),
            Question(
                question="Was ist der Fluch der Dimensionalität im Feature-Selection-Kontext?",
                answer="Der Fluch der Dimensionalität bei der Feature Selection beschreibt die Probleme, die durch hochdimensionale Daten entstehen, z.B. erhöhte Rechenkomplexität und Schwierigkeiten, sinnvolle Features zu finden.",
            ),
            Question(
                question="Was ist der Unterschied zwischen L1- und L2-Regularisierung?",
                answer="L1-Regularisierung (Lasso) fügt einen Term proportional zu den Beträgen der Koeffizienten hinzu und fördert Sparsity, L2-Regularisierung (Ridge) fügt einen Term proportional zum Quadrat der Koeffizienten hinzu und bestraft große Koeffizienten.",
            ),
            Question(
                question="Was ist der Zweck von Kreuzvalidierung bei Feature Selection?",
                answer="Kreuzvalidierung hilft, die Leistung eines Modells mit unterschiedlichen Feature-Subsets zu bewerten, um die informativsten Features zu identifizieren und Overfitting zu reduzieren.",
            ),
            Question(
                question="Was ist die Rolle von Bias bei der Modellevaluation?",
                answer="Bias in der Modellevaluation bezieht sich auf systematische Fehler oder Ungenauigkeiten in den Vorhersagen eines Modells, die aus vereinfachenden Annahmen oder Modellbeschränkungen entstehen.",
            ),
            Question(
                question="Warum ist Interpretierbarkeit in Machine-Learning-Modellen wichtig?",
                answer="Interpretierbarkeit ist wichtig, um zu verstehen, wie Vorhersagen getroffen werden, Einblicke in Zusammenhänge zu gewinnen und Vertrauen bei Stakeholdern aufzubauen.",
            ),
            Question(
                question="Was ist der Unterschied zwischen k-Means und hierarchischem Clustering?",
                answer="k-Means partitioniert Daten in k Cluster, während hierarchisches Clustering eine Baumstruktur erstellt, indem Cluster rekursiv zusammengeführt oder geteilt werden.",
            ),
            Question(
                question="Wozu dient die Elbow-Methode beim k-Means-Clustering?",
                answer="Die Elbow-Methode wird verwendet, um die optimale Anzahl von Clustern (k) zu bestimmen, indem man die Summe der quadratischen Abweichungen gegen k aufträgt und den Punkt identifiziert, an dem die Abnahme langsamer wird.",
            ),
            Question(
                question="Welche Rolle spielt Regularisierung bei der Reduzierung der Modellkomplexität?",
                answer="Regularisierung reduziert die Modellkomplexität, indem Strafterme zur Verlustfunktion hinzugefügt werden, um einfachere Modelle mit kleineren Koeffizienten oder weniger Features zu fördern.",
            ),
            Question(
                question="Was ist der Unterschied zwischen Gradient Descent und Stochastic Gradient Descent?",
                answer="Gradient Descent aktualisiert Parameter mit dem Durchschnittsgradienten über den gesamten Trainingsdatensatz, SGD verwendet den Gradienten eines zufällig ausgewählten Datenpunkts oder Mini-Batches.",
            ),
            Question(
                question="Was ist der Tradeoff zwischen Bias und Varianz bei der Modellauswahl?",
                answer="Der Tradeoff umfasst die Balance zwischen Bias (Underfitting) und Varianz (Overfitting), indem Modelle mit angemessener Komplexität gewählt werden.",
            ),
            Question(
                question="Welche Rolle spielt Regularisierung bei der Vermeidung von Overfitting?",
                answer="Regularisierung verhindert Overfitting, indem sie übermäßig komplexe Modelle bestraft und einfachere Modelle fördert, die besser auf unbekannte Daten generalisieren.",
            ),
            Question(
                question="Wie geht man mit unausgeglichenen Datensätzen in Klassifikationsaufgaben um?",
                answer="Methoden umfassen Oversampling der Minderheitsklasse, Undersampling der Mehrheitsklasse, kosten-sensitive Algorithmen oder synthetische Daten mit SMOTE.",
            ),
            Question(
                question="Wozu dient A/B-Testing im Data Science?",
                answer="A/B-Testing vergleicht zwei oder mehr Versionen eines Produkts oder Eingriffs, um zu bestimmen, welche Version anhand vorher definierter Metriken besser abschneidet.",
            ),
            Question(
                question="Was ist der Unterschied zwischen Korrelation und Kausalität?",
                answer="Korrelation misst die Stärke und Richtung der linearen Beziehung zwischen zwei Variablen, Kausalität zeigt, dass eine Veränderung in einer Variablen direkt eine Veränderung in einer anderen verursacht.",
            ),
            Question(
                question="Welche Rolle spielt Feature Scaling im Machine Learning?",
                answer="Feature Scaling stellt sicher, dass alle Features den gleichen Maßstab haben, um Dominanz einzelner Features während des Trainings zu verhindern.",
            ),
            Question(
                question="Was ist der Unterschied zwischen Klassifikation und Clustering?",
                answer="Klassifikation ist überwacht und sagt Klassen voraus, Clustering ist unüberwacht und gruppiert ähnliche Datenpunkte.",
            ),
            Question(
                question="Wozu dient Principal Component Analysis (PCA)?",
                answer="PCA reduziert die Dimensionalität, indem die ursprünglichen Features in orthogonale Hauptkomponenten transformiert werden, die die maximale Varianz erfassen.",
            ),
            Question(
                question="Welche Rolle spielt Regularisierung in neuronalen Netzen?",
                answer="Regularisierung verhindert Overfitting durch Hinzufügen von Straftermen zur Verlustfunktion, um einfachere Netzwerke zu erzwingen.",
            ),
            Question(
                question="Was ist Dropout-Regularisierung?",
                answer="Dropout entfernt zufällig Neuronen während des Trainings, um robustere Repräsentationen zu erzwingen und Overfitting zu reduzieren.",
            ),
            Question(
                question="Was ist der Unterschied zwischen GANs und VAEs?",
                answer="GANs bestehen aus Generator und Diskriminator, die gegeneinander arbeiten, VAEs lernen eine probabilistische Repräsentation des latenten Raums und generieren neue Daten aus dieser.",
            ),
            Question(
                question="Was ist der Unterschied zwischen Batch-Gradient-Descent und Mini-Batch-Gradient-Descent?",
                answer="Batch-Gradient-Descent verwendet den gesamten Trainingsdatensatz pro Schritt, Mini-Batch-Gradient-Descent nutzt zufällige Teilmengen (Mini-Batches).",
            ),
            Question(
                question="Welche Rolle spielen Aktivierungsfunktionen in neuronalen Netzen?",
                answer="Aktivierungsfunktionen führen Nichtlinearität ein, damit das Netz komplexe Abbildungen lernen kann; Beispiele: sigmoid, tanh, ReLU, softmax.",
            ),
            Question(
                question="Was ist der Unterschied zwischen generativen und diskriminativen Modellen?",
                answer="Generative Modelle lernen die gemeinsame Verteilung von Eingaben und Ziel, diskriminative Modelle lernen die bedingte Verteilung des Ziels gegeben der Eingaben.",
            ),
            Question(
                question="Wozu dient Dropout-Regularisierung in neuronalen Netzen?",
                answer="Dropout reduziert Overfitting, indem zufällig Neuronen entfernt werden und robustere Repräsentationen erzwungen werden.",
            ),
            Question(
                question="Welche Rolle spielen LSTMs in Sequenzmodellen?",
                answer="LSTMs sind RNNs, die langfristige Abhängigkeiten erfassen, geeignet für Sprachmodellierung und Zeitreihen.",
            ),
            Question(
                question="Was ist der Unterschied zwischen Precision und Recall in Klassifikationsaufgaben?",
                answer="Precision misst Anteil richtig positiver Vorhersagen an allen positiven Vorhersagen, Recall misst Anteil richtig positiver Vorhersagen an allen tatsächlichen positiven Instanzen.",
            ),
            Question(
                question="Was ist der F1-Score und wozu ist er nützlich?",
                answer="Der F1-Score ist das harmonische Mittel von Precision und Recall, besonders nützlich bei unausgeglichenen Datensätzen.",
            ),
            Question(
                question="Wozu dienen Wort-Embeddings in NLP?",
                answer="Wort-Embeddings repräsentieren Wörter als dichte Vektoren, erfassen semantische Beziehungen und erleichtern Verarbeitung durch neuronale Netze.",
            ),
            Question(
                question="Was ist der Unterschied zwischen Word2Vec und GloVe?",
                answer="Word2Vec lernt Embeddings durch Vorhersage der umliegenden Wörter, GloVe durch Faktorisierung der Ko-Okkurrenzmatrix.",
            ),
            Question(
                question="Wozu dient Sentiment-Analyse in NLP?",
                answer="Sentiment-Analyse erkennt die Stimmung oder Meinung in Texten, z.B. positiv, negativ oder neutral.",
            ),
            Question(
                question="Was ist der Unterschied zwischen shallow und deep learning?",
                answer="Shallow Learning nutzt wenige Schichten/Features, Deep Learning verwendet tiefe neuronale Netze, um hierarchische Repräsentationen zu lernen.",
            ),
            Question(
                question="Was ist der Unterschied zwischen Precision und Accuracy?",
                answer="Precision misst korrekt positive Vorhersagen unter allen positiven Vorhersagen, Accuracy misst korrekt Vorhersagen insgesamt.",
            ),
            Question(
                question="Was ist der Unterschied zwischen k-fold und leave-one-out Kreuzvalidierung?",
                answer="K-fold teilt Daten in k Teile und trainiert k-mal, leave-one-out lässt jeweils einen Punkt aus, trainiert k-mal.",
            ),
            Question(
                question="Was ist der Naive-Bayes-Klassifikator und wie funktioniert er?",
                answer="Naive Bayes basiert auf Bayes-Theorem mit der Annahme unabhängiger Features; Berechnet die Wahrscheinlichkeit einer Klasse gegeben Eingaben.",
            ),
            Question(
                question="Was ist der Unterschied zwischen Korrelation und Kovarianz?",
                answer="Kovarianz misst, wie zwei Variablen gemeinsam variieren, Korrelation normiert dies auf [-1,1] und zeigt Stärke und Richtung.",
            ),
            Question(
                question="Wozu dient eine Konfusionsmatrix?",
                answer="Visualisiert die Leistung eines Klassifikators, zeigt TP, TN, FP, FN.",
            ),
            Question(
                question="Was ist der Unterschied zwischen stratified sampling und random sampling?",
                answer="Stratified Sampling teilt Population in homogene Schichten und sampelt proportional, Random Sampling wählt zufällig aus.",
            ),
            Question(
                question="Was ist der Unterschied zwischen univariater, bivariater und multivariater Analyse?",
                answer="Univariat: einzelne Variable, bivariant: zwei Variablen, multivariat: mehrere Variablen gleichzeitig.",
            ),
            Question(
                question="Wozu dient Datenvorverarbeitung im Machine Learning?",
                answer="Reinigen, transformieren und vorbereiten von Rohdaten; z.B. Umgang mit fehlenden Werten, Kodierung kategorischer Variablen, Skalierung.",
            ),
            Question(
                question="Was ist der Bias eines statistischen Schätzers?",
                answer="Bias misst Differenz zwischen erwartetem Wert des Schätzers und dem wahren Parameter; systematische Über- oder Unterschätzung.",
            ),
            Question(
                question="Was ist die Varianz eines statistischen Schätzers?",
                answer="Varianz misst die Streuung der Schätzerwerte um ihren Erwartungswert; hohe Varianz = weit gestreut, niedrige Varianz = eng gebündelt.",
            ),
            Question(
                question="Was ist der Unterschied zwischen parametrischen und nicht-parametrischen Tests?",
                answer="Parametrisch: Annahme einer spezifischen Verteilung, nicht-parametrisch: keine Verteilungsannahme, basiert auf Rängen oder Häufigkeiten.",
            ),
            Question(
                question="Wozu dient Feature Scaling im Machine Learning?",
                answer="Stellt gleiche Skala für alle Features sicher; verhindert Dominanz bestimmter Features; z.B. Min-Max-Skalierung, Standardisierung.",
            ),
            Question(
                question="Was ist der Unterschied zwischen Korrelation und Kausalität?",
                answer="Korrelation misst Stärke und Richtung der Beziehung, Kausalität zeigt direkte Ursache-Wirkung.",
            ),
            Question(
                question="Was ist der zentrale Grenzwertsatz und warum ist er wichtig?",
                answer="Zentraler Grenzwertsatz: Stichprobenmittelwerte nähern sich Normalverteilung bei wachsender Stichprobe; wichtig für Schlussfolgerungen über Populationen.",
            ),
            Question(
                question="Wozu dient Outlier Detection?",
                answer="Erkennt Werte, die stark von anderen abweichen; verhindert Verzerrungen in Analysen und Modellen.",
            ),
            Question(
                question="Unterschied zwischen überwachten und unüberwachten Outlier Detection-Methoden?",
                answer="Überwacht: gelabelte Daten, Unüberwacht: nur Eigenschaften der Daten.",
            ),
            Question(
                question="Unterschied zwischen statistischer Inferenz und prädiktiver Modellierung?",
                answer="Inferenz: Schlussfolgerungen über Population, prädiktive Modellierung: Vorhersagen über neue Daten.",
            ),
            Question(
                question="Wozu dient Regularisierung im Machine Learning?",
                answer="Verhindert Overfitting, indem Strafterme hinzugefügt werden; häufig L1 oder L2.",
            ),
            Question(
                question="Unterschied zwischen Batch-Gradient-Descent und Stochastic Gradient Descent?",
                answer="Batch: ganzes Dataset, SGD: einzelne oder Mini-Batches.",
            ),
            Question(
                question="Unterschied zwischen statistischem Modellieren und Machine Learning?",
                answer="Statistik: Beziehungen verstehen, Machine Learning: Muster erkennen und Vorhersagen treffen.",
            ),
            Question(
                question="Wozu dient Feature Selection?",
                answer="Auswahl der relevantesten Features zur Leistungssteigerung, Vermeidung von Overfitting, bessere Interpretierbarkeit.",
            ),
            Question(
                question="Unterschied zwischen Regularisierung und Feature Selection?",
                answer="Regularisierung bestraft komplexe Modelle, Feature Selection wählt aktiv die wichtigsten Features aus.",
            ),
            Question(
                question="Unterschied zwischen Grid Search und Random Search für Hyperparameter?",
                answer="Grid Search: exhaustiv durch Gitter, Random Search: zufällige Auswahl aus Verteilung.",
            ),
            Question(
                question="Wozu dient Kreuzvalidierung bei der Modellevaluation?",
                answer="Bewertet Modellleistung, schätzt Generalisierungsfehler, erkennt Overfitting.",
            ),
            Question(
                question="Unterschied zwischen Precision und Recall in Klassifikations-Evaluation?",
                answer="Precision: Anteil richtig positiver Vorhersagen an allen positiven Vorhersagen; Recall: Anteil richtig positiver Vorhersagen an allen tatsächlichen Positiven.",
            ),
            Question(
                question="Was ist der F1-Score und warum ist er bei unausgeglichenen Datensätzen nützlich?",
                answer="Der F1-Score ist das harmonische Mittel von Precision und Recall und bietet eine einzelne Metrik zur Bewertung der Leistung eines Klassifikators. Er ist besonders nützlich bei unausgeglichenen Datensätzen, bei denen eine Klasse deutlich häufiger vorkommt als andere.",
            ),
            Question(
                question="Was ist der Unterschied zwischen Bagging- und Boosting-Ensemble-Methoden?",
                answer="Bagging (Bootstrap Aggregating) erstellt mehrere Modelle unabhängig und kombiniert ihre Vorhersagen durch Mittelung oder Abstimmung, während Boosting Modelle sequenziell aufbaut und dabei mehr Gewicht auf falsch klassifizierte Instanzen legt.",
            ),
            Question(
                question="Wozu dient die Hauptkomponentenanalyse (PCA) bei der Dimensionsreduktion?",
                answer="PCA reduziert die Dimensionalität eines Datensatzes, indem die ursprünglichen Features in eine neue Menge orthogonaler Hauptkomponenten transformiert werden, die die maximale Varianz der Daten erfassen.",
            ),
            Question(
                question="Was ist der Unterschied zwischen k-Means- und hierarchischem Clustering?",
                answer="K-Means partitioniert Daten in k Cluster, indem die Summe der quadrierten Abweichungen innerhalb der Cluster minimiert wird, während hierarchisches Clustering eine Baumstruktur von Clustern erstellt, indem Cluster rekursiv zusammengeführt oder geteilt werden.",
            ),
            Question(
                question="Was ist der Unterschied zwischen Klassifikation und Regression im Machine Learning?",
                answer="Klassifikation ist eine überwachte Lernaufgabe, bei der kategoriale Labels vorhergesagt werden, während Regression eine überwachte Lernaufgabe ist, bei der kontinuierliche numerische Werte vorhergesagt werden.",
            ),
            Question(
                question="Wozu dient Natural Language Processing (NLP) in Data Science?",
                answer="NLP ist ein Bereich der künstlichen Intelligenz, der sich mit der Interaktion zwischen Computern und menschlicher Sprache beschäftigt. Es ermöglicht Computern, menschliche Sprache zu verstehen, zu interpretieren und zu generieren.",
            ),
            Question(
                question="Was ist der Unterschied zwischen Bag-of-Words und Wort-Embeddings in NLP?",
                answer="Bag-of-Words repräsentiert Text als Sammlung von Wortzählungen oder Häufigkeiten und ignoriert Reihenfolge und Grammatik, während Wort-Embeddings Wörter als dichte Vektoren in einem kontinuierlichen Raum darstellen und semantische Beziehungen erfassen.",
            ),
            Question(
                question="Was ist der Unterschied zwischen Sentiment-Analyse und Topic Modeling in NLP?",
                answer="Sentiment-Analyse bestimmt die Stimmung oder Meinung in einem Text (z.B. positiv, negativ, neutral), während Topic Modeling die zugrundeliegenden Themen oder Inhalte in einer Dokumentensammlung identifiziert.",
            ),
            Question(
                question="Wozu dient Word2Vec in NLP?",
                answer="Word2Vec ist ein Modell, das Wort-Embeddings durch Vorhersage benachbarter Wörter in einem Textkorpus lernt. Es erfasst semantische Beziehungen zwischen Wörtern und erleichtert die Verarbeitung von Textdaten durch Algorithmen.",
            ),
            Question(
                question="Was ist der Unterschied zwischen generativen und diskriminativen Modellen im Machine Learning?",
                answer="Generative Modelle lernen die gemeinsame Wahrscheinlichkeitsverteilung von Eingabefeatures und Zielvariablen, während diskriminative Modelle die bedingte Verteilung der Zielvariablen gegeben der Eingaben lernen.",
            ),
            Question(
                question="Was ist der Unterschied zwischen Deep Learning und traditionellen Machine-Learning-Algorithmen?",
                answer="Deep Learning nutzt neuronale Netze mit mehreren Schichten, die hierarchische Repräsentationen der Daten lernen, während traditionelle Machine-Learning-Algorithmen meist auf handgefertigten Features und einfacheren Modellen basieren.",
            ),
            Question(
                question="Wozu dient Transfer Learning im Deep Learning?",
                answer="Transfer Learning ist eine Technik, bei der ein Modell, das auf einer Aufgabe trainiert wurde, als Ausgangspunkt für ein Modell auf einer verwandten Aufgabe verwendet wird. Es ermöglicht die Übertragung von Wissen und Features und reduziert den Bedarf an großen gelabelten Datensätzen.",
            ),
            Question(
                question="Was ist der Unterschied zwischen Convolutional Neural Networks (CNNs) und Recurrent Neural Networks (RNNs)?",
                answer="CNNs eignen sich gut für die Verarbeitung von gitterartigen Daten wie Bildern, während RNNs für sequenzielle Daten mit zeitlichen Abhängigkeiten wie Text oder Zeitreihen entwickelt wurden.",
            ),
            Question(
                question="Wozu dient Batch-Normalisierung in neuronalen Netzen?",
                answer="Batch-Normalisierung verbessert die Trainingsstabilität und -geschwindigkeit, indem die Aktivierungen jeder Schicht normalisiert werden. Sie reduziert interne Kovariatenverschiebungen und beschleunigt die Konvergenz.",
            ),
            Question(
                question="Was ist der Unterschied zwischen Feedforward- und Recurrent Neural Networks?",
                answer="Ein Feedforward-Netz besteht aus Schichten von Neuronen ohne Zyklen, während ein RNN Verbindungen hat, die Zyklen bilden, sodass es Zustand oder Gedächtnis über die Zeit beibehalten kann.",
            ),
            Question(
                question="Wozu dient Dropout-Regularisierung in neuronalen Netzen?",
                answer="Dropout-Regularisierung verhindert Überanpassung, indem während des Trainings zufällig ein Teil der Neuronen deaktiviert wird. Das zwingt das Netzwerk, robustere Repräsentationen zu lernen.",
            ),
            Question(
                question="Was ist der Unterschied zwischen LSTMs und GRUs in RNNs?",
                answer="LSTMs und GRUs sind RNN-Architekturen, die Langzeitabhängigkeiten erfassen, unterscheiden sich aber in ihren internen Gate-Mechanismen und der Rechenkomplexität.",
            ),
            Question(
                question="Wozu dienen Attention-Mechanismen in neuronalen Netzen?",
                answer="Attention-Mechanismen ermöglichen es dem Modell, sich auf relevante Teile der Eingabedaten zu konzentrieren und irrelevante Informationen zu ignorieren. Besonders erfolgreich in NLP-Aufgaben wie maschineller Übersetzung.",
            ),
            Question(
                question="Was ist der Unterschied zwischen GANs und Autoencodern im Deep Learning?",
                answer="GANs bestehen aus Generator- und Diskriminatornetzwerken, die gegeneinander antreten, um realistische Daten zu erzeugen, während Autoencoder aus Encoder- und Decoder-Netzwerken bestehen, die Eingabedaten rekonstruieren.",
            ),
            Question(
                question="Wozu dient Reinforcement Learning im Machine Learning?",
                answer="Reinforcement Learning ist ein Paradigma, bei dem ein Agent durch Interaktion mit einer Umgebung lernt, Entscheidungen zu treffen, um kumulative Belohnungen zu maximieren.",
            ),
            Question(
                question="Was ist der Unterschied zwischen Q-Learning und Policy-Gradient-Methoden?",
                answer="Q-Learning lernt eine optimale Aktionswahlpolitik durch iterative Aktualisierung einer Q-Funktion, während Policy-Gradient-Methoden die Politik direkt parametrisieren und anhand von Gradienten erwarteter Belohnungen aktualisieren.",
            ),
            Question(
                question="Wozu dient Datenvorverarbeitung in der explorativen Datenanalyse (EDA)?",
                answer="Datenvorverarbeitung umfasst das Bereinigen, Transformieren und Vorbereiten von Rohdaten für die Analyse, z.B. Umgang mit fehlenden Werten, Entfernen von Ausreißern und Kodierung kategorialer Variablen.",
            ),
            Question(
                question="Welche gängigen Techniken gibt es für den Umgang mit fehlenden Daten in EDA?",
                answer="Gängige Techniken sind Imputation (Ersetzen fehlender Werte durch Schätzungen), Löschung (Entfernen von Zeilen/Spalten mit fehlenden Werten) und Vorhersage (Schätzung fehlender Werte durch Modelle).",
            ),
            Question(
                question="Was ist der Unterschied zwischen univariater und bivariater Analyse in EDA?",
                answer="Univariate Analyse untersucht die Verteilung und Kennzahlen einer einzelnen Variablen, während bivariate Analyse Beziehungen zwischen zwei Variablen untersucht.",
            ),
            Question(
                question="Wozu dient Datenvisualisierung in EDA?",
                answer="Datenvisualisierung hilft, Struktur, Muster und Zusammenhänge in den Daten zu erkennen. Sie liefert Einblicke, die aus Rohdaten oder Zusammenfassungen allein nicht ersichtlich sind.",
            ),
            Question(
                question="Welche gängigen Arten von Datenvisualisierung werden in EDA verwendet?",
                answer="Histogramme, Streudiagramme, Boxplots, Balkendiagramme, Liniendiagramme und Heatmaps.",
            ),
            Question(
                question="Was ist der Unterschied zwischen kontinuierlichen und kategorialen Variablen in EDA?",
                answer="Kontinuierliche Variablen sind numerisch mit unendlichen möglichen Werten in einem Bereich, kategoriale Variablen sind qualitativ mit endlichen Kategorien.",
            ),
            Question(
                question="Wozu dienen statistische Zusammenfassungen in EDA?",
                answer="Statistische Zusammenfassungen liefern Kennzahlen wie Mittelwert, Median, Modus, Varianz und Perzentile, um zentrale Tendenz, Streuung und Verteilung zu beschreiben.",
            ),
            Question(
                question="Was ist der Unterschied zwischen Maßzahlen der zentralen Tendenz und der Streuung in EDA?",
                answer="Zentrale Tendenz beschreibt typische Werte (Mittelwert, Median, Modus), Streuung misst die Variabilität der Daten (Varianz, Standardabweichung).",
            ),
            Question(
                question="Wozu dient Hypothesentesten in EDA?",
                answer="Hypothesentests bewerten, ob beobachtete Unterschiede oder Zusammenhänge statistisch signifikant sind oder zufällig auftreten. Null- und Alternativhypothesen werden formuliert und getestet.",
            ),
            Question(
                question="Was ist der Unterschied zwischen parametrischen und nicht-parametrischen Tests?",
                answer="Parametrische Tests setzen eine spezifische Wahrscheinlichkeitsverteilung voraus (z.B. Normalverteilung), nicht-parametrische Tests basieren auf Rängen oder Häufigkeiten ohne Verteilungsannahmen.",
            ),
            Question(
                question="Wozu dient Korrelationsanalyse in EDA?",
                answer="Korrelationsanalyse misst Stärke und Richtung der linearen Beziehung zwischen zwei kontinuierlichen Variablen und identifiziert Muster und Zusammenhänge.",
            ),
            Question(
                question="Was ist der Unterschied zwischen Pearson- und Spearman-Korrelation?",
                answer="Pearson misst lineare Beziehungen, Spearman monotone Beziehungen, auch nicht-linear.",
            ),
            Question(
                question="Wozu dient Regressionsanalyse in EDA?",
                answer="Regressionsanalyse modelliert die Beziehung zwischen unabhängigen Variablen und einer abhängigen Variable, um Effekte der Prädiktoren zu verstehen.",
            ),
            Question(
                question="Welche Annahmen gelten für lineare Regression in EDA?",
                answer="Lineare Beziehung, Unabhängigkeit der Residuen, Homoskedastizität, Normalverteilung der Residuen.",
            ),
            Question(
                question="Was ist der Unterschied zwischen einfacher und multipler linearer Regression?",
                answer="Einfache Regression: eine unabhängige Variable; multiple Regression: mehrere unabhängige Variablen.",
            ),
            Question(
                question="Wozu dient logistische Regression in EDA?",
                answer="Modellierung der Beziehung zwischen Prädiktoren und einer binären Zielvariable (0/1) für Klassifikationsaufgaben.",
            ),
            Question(
                question="Welche Annahmen gelten für logistische Regression in EDA?",
                answer="Lineare Beziehung zwischen Prädiktoren und Log-Odds, unabhängige Beobachtungen, keine starke Multikollinearität.",
            ),
            Question(
                question="Wozu dient Ausreißererkennung in EDA?",
                answer="Ausreißererkennung identifiziert Beobachtungen, die stark von anderen abweichen, um Verzerrungen in Analysen und Modellen zu vermeiden.",
            ),
            Question(
                question="Welche Techniken gibt es zur Ausreißererkennung in EDA?",
                answer="Grafische Methoden (Scatterplots, Boxplots), statistische Methoden (Z-Score, modifizierter Z-Score), Nähe-basierte Methoden (Nearest Neighbors).",
            ),
            Question(
                question="Wozu dienen Boxplots in EDA?",
                answer="Boxplots visualisieren Verteilung, zentrale Tendenz und Streuung, zeigen Median, Quartile und Ausreißer.",
            ),
            Question(
                question="Wozu dienen Histogramme in EDA?",
                answer="Histogramme zeigen die Häufigkeitsverteilung kontinuierlicher Variablen durch Einteilung in Intervalle (Bins).",
            ),
            Question(
                question="Wozu dienen Streudiagramme in EDA?",
                answer="Streudiagramme visualisieren die Beziehung zwischen zwei kontinuierlichen Variablen und zeigen Muster, Trends und Korrelationen.",
            ),
            Question(
                question="Wozu dienen Balkendiagramme in EDA?",
                answer="Balkendiagramme stellen kategoriale Daten durch Balkenhöhen dar und ermöglichen Vergleich der Verteilung.",
            ),
            Question(
                question="Wozu dienen Liniendiagramme in EDA?",
                answer="Liniendiagramme zeigen Trends oder Muster über Zeit oder kontinuierliche Dimensionen, z.B. für Zeitreihenanalyse.",
            ),
            Question(
                question="Wozu dienen Heatmaps in EDA?",
                answer="Heatmaps visualisieren Magnituden oder Beziehungen zwischen Variablen durch Farben und helfen, Muster in großen Datensätzen zu erkennen.",
            ),
            Question(
                question="Wozu dienen Korrelationsmatrizen in EDA?",
                answer="Korrelationsmatrizen zeigen paarweise Korrelationen zwischen Variablen in Tabellen- oder Heatmap-Form und helfen, Muster zu erkennen.",
            ),
            Question(
                question="Was ist der Unterschied zwischen Korrelation und Kausalität?",
                answer="Korrelation misst Stärke und Richtung einer linearen Beziehung, Kausalität zeigt, dass Änderungen einer Variablen direkt Änderungen der anderen verursachen. Korrelation impliziert keine Kausalität.",
            ),
            Question(
                question="Wozu dienen statistische Tests in EDA?",
                answer="Statistische Tests bewerten Signifikanz von Unterschieden oder Zusammenhängen und ermöglichen Rückschlüsse auf Populationen.",
            ),
            Question(
                question="Was ist der Unterschied zwischen parametrischen und nicht-parametrischen Tests in EDA?",
                answer="Parametrische Tests setzen bestimmte Wahrscheinlichkeitsverteilungen voraus, nicht-parametrische Tests basieren auf Rängen oder Häufigkeiten.",
            ),
            Question(
                question="Wozu dient ANOVA in EDA?",
                answer="ANOVA vergleicht Mittelwerte von zwei oder mehr Gruppen auf signifikante Unterschiede, z.B. bei mehreren Kategorien oder Behandlungen.",
            ),
            Question(
                question="Was ist der Unterschied zwischen Einweg- und Zweiweg-ANOVA?",
                answer="Einweg-ANOVA vergleicht Mittelwerte nach einem Faktor, Zweiweg-ANOVA betrachtet Effekte von zwei Faktoren (Haupteffekte und Interaktion).",
            ),
            Question(
                question="Wozu dient der Chi-Quadrat-Test in EDA?",
                answer="Der Chi-Quadrat-Test prüft die Unabhängigkeit zweier kategorialer Variablen durch Vergleich beobachteter und erwarteter Häufigkeiten.",
            ),
            Question(
                question="Wozu dienen T-Tests in EDA?",
                answer="T-Tests vergleichen Mittelwerte zweier unabhängiger Stichproben oder einer Stichprobe mit einem bekannten Wert und prüfen Signifikanz.",
            ),
            Question(
                question="Was ist der Unterschied zwischen unabhängigen und gepaarten T-Tests?",
                answer="Unabhängige T-Tests vergleichen zwei unabhängige Gruppen, gepaarte T-Tests vergleichen zwei verwandte Gruppen (z.B. Vorher-Nachher-Messungen).",
            ),
            Question(
                question="Wozu dienen nicht-parametrische Tests in EDA?",
                answer="Nicht-parametrische Tests werden verwendet, wenn die Voraussetzungen parametrischer Tests nicht erfüllt sind und bieten robuste Alternativen für nicht-normalverteilte oder schiefe Daten.",
            ),
            Question(
                question="Was ist der Unterschied zwischen Wilcoxon- und Mann-Whitney-Tests?",
                answer="Wilcoxon vergleicht Mediane zweier verwandter Gruppen, Mann-Whitney vergleicht Mediane zweier unabhängiger Gruppen.",
            ),
            Question(
                question="Wozu dient Explorative Faktorenanalyse (EFA) in EDA?",
                answer="EFA identifiziert zugrunde liegende Faktoren oder latente Variablen, die gemeinsame Varianz erklären, und deckt Strukturen im Datensatz auf.",
            ),
            Question(
                question="Was ist der Unterschied zwischen EFA und PCA in EDA?",
                answer="EFA identifiziert zugrunde liegende Faktoren, PCA erfasst maximale Varianz mit orthogonalen Hauptkomponenten.",
            ),
            Question(
                question="Wozu dient Clusteranalyse in EDA?",
                answer="Clusteranalyse identifiziert Gruppen ähnlicher Beobachtungen, deckt natürliche Gruppierungen auf und zeigt Muster.",
            ),
            Question(
                question="Welche Algorithmen werden häufig für Clusteranalyse in EDA verwendet?",
                answer="K-Means, hierarchisches Clustering, DBSCAN, Gaussian Mixture Models.",
            ),
            Question(
                question="Was ist der Unterschied zwischen K-Means und hierarchischem Clustering in EDA?",
                answer="K-Means minimiert innerhalb-Cluster-Quadratsummen, hierarchisches Clustering erstellt Baumstruktur durch rekursives Zusammenführen/Teilen.",
            ),
            Question(
                question="Wozu dient ein Dendrogramm in hierarchischem Clustering?",
                answer="Dendrogramme visualisieren hierarchische Beziehungen, zeigen Merge-Reihenfolge und Abstände, helfen optimale Clusterzahl zu bestimmen.",
            ),
            Question(
                question="Wozu dient Silhouette-Analyse in Cluster-Validierung?",
                answer="Silhouette-Analyse bewertet Qualität von Clustern durch Kohäsion innerhalb und Trennung zwischen Clustern. Höhere Werte = besser definierte Cluster.",
            ),
            Question(
                question="Wozu dienen Dimensionsreduktionstechniken in EDA?",
                answer="Reduzieren Anzahl der Features, bewahren wichtigste Informationen, überwinden Fluch der Dimensionalität, verbessern Rechenleistung.",
            ),
            Question(
                question="Welche Dimensionsreduktionstechniken werden häufig verwendet?",
                answer="PCA, Faktorenanalyse, t-SNE, LDA.",
            ),
            Question(
                question="Wozu dient PCA in EDA?",
                answer="PCA reduziert Dimensionalität durch Transformation in orthogonale Hauptkomponenten und zeigt Muster in hochdimensionalen Daten.",
            ),
            Question(
                question="Was ist der Unterschied zwischen PCA und Faktorenanalyse in EDA?",
                answer="PCA erfasst maximale Varianz, Faktorenanalyse identifiziert zugrunde liegende Faktoren, die gemeinsame Varianz erklären.",
            ),
            Question(
                question="Wozu dient t-SNE in EDA?",
                answer="t-SNE visualisiert hochdimensionale Daten in niedrigdimensionalem Raum, bewahrt lokale Strukturen und Muster, häufig für Clustervisualisierung.",
            ),
            Question(
                question="Was ist der Unterschied zwischen LDA und PCA in EDA?",
                answer="LDA maximiert Trennung zwischen Klassen bei Dimensionsreduktion, PCA fokussiert auf maximale Varianz unabhängig von Klassen.",
            ),
            Question(
                question="Wozu dient Feature Selection in EDA?",
                answer="Feature Selection wählt relevanteste Features, verbessert Modellleistung, reduziert Overfitting, erhöht Interpretierbarkeit.",
            ),
            Question(
                question="Welche Techniken zur Feature Selection werden in EDA verwendet?",
                answer="Filter-Methoden (Korrelation, Informationsgewinn), Wrapper-Methoden (rekursive Merkmalselimination), Embedded-Methoden (LASSO, Entscheidungsbäume).",
            ),
            Question(
                question="Wozu dienen Ensemble-Methoden in EDA?",
                answer="Kombinieren mehrere Modelle, verbessern Vorhersageleistung, Robustheit und Generalisierung, reduzieren Overfitting.",
            ),
            Question(
                question="Welche Ensemble-Methoden werden häufig verwendet?",
                answer="Bagging, Boosting (AdaBoost, Gradient Boosting), Stacking.",
            ),
            Question(
                question="Wozu dient Modellevaluation in EDA?",
                answer="Bewertung von Modellleistung mit Metriken, zur Bestimmung, wie gut Muster erkannt und Vorhersagen gemacht werden.",
            ),
            Question(
                question="Welche gängigen Evaluationsmetriken für Klassifikation werden verwendet?",
                answer="Accuracy, Precision, Recall, F1-Score, ROC-AUC.",
            ),
            Question(
                question="Welche gängigen Evaluationsmetriken für Regression werden verwendet?",
                answer="Mean Squared Error (MSE), Root Mean Squared Error (RMSE), Mean Absolute Error (MAE), R²-Score.",
            ),
        ]

        # Beispiel-User
        users = [
            User(username="admin", password_hash="hashed123", role="admin"),
            User(username="user", password_hash="hashed456", role="user"),
        ]

        session.add_all(questions + users)
        await session.commit()

    print("Seed completed.")


if __name__ == "__main__":
    asyncio.run(seed())
