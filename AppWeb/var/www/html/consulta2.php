<!DOCTYPE html>
<html>
<head
    <title>Consulta: Jugador con mayor trofeos por Brawler</title>
    <link rel="stylesheet" href="styles3.css">
</head>
<body>
    <?php
    try {
        $pdo = new PDO('pgsql:host=localhost;port=5432;dbname=cc3201', 'webuser', '12brawl13');
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

        if (!isset($_GET['nombre_brawler']) || empty(trim($_GET['nombre_brawler']))) {
            die("Error: No se proporcion   un brawler v  lido.");
        }
        if (!isset($_GET['nombre_mes']) || empty(trim($_GET['nombre_mes']))) {
            die("Error: No se proporcion   un mes v  lido.");
        }

        $nombre_brawler = trim($_GET['nombre_brawler']);
        $nombre_mes = trim($_GET['nombre_mes']);

        $stmt = $pdo->prepare("
            SELECT tag_jugador, trofeos
            FROM ProyectBrawlStars.JuegaCon
            WHERE nombre_brawler = :nombre_brawler
              AND nombre_mes = :nombre_mes
              AND trofeos = (
                SELECT MAX(trofeos)
                FROM ProyectBrawlStars.JuegaCon
                WHERE nombre_brawler = :nombre_brawler AND nombre_mes = :nombre_mes
              );
        ");

        $stmt->execute([
            'nombre_brawler' => $nombre_brawler,
            'nombre_mes' => $nombre_mes,
        ]);
        $result = $stmt->fetchAll(PDO::FETCH_ASSOC);

        // Mostrar resultados
        echo "<h3>Resultados para el Brawler: " . htmlspecialchars($nombre_brawler) . " y Mes: " . htmlspecialchars($nombre_mes) . "</h3>";
        echo "<table>
                <tr>
                    <th>Tag del Jugador</th>
                    <th>Trofeos</th>
                </tr>";

        if (count($result) > 0) {
            foreach ($result as $row) {
                echo "<tr>
                        <td>" . htmlspecialchars($row['tag_jugador']) . "</td>
                        <td>" . htmlspecialchars($row['trofeos']) . "</td>
                      </tr>";
            }
        } else {
            echo "<tr><td colspan='2'>No se encontraron datos para el Brawler y Mes ingresados.</td></tr>";
        }
        echo "</table>";
    } catch (PDOException $e) {
        echo "Error: " . $e->getMessage();
    }
    ?>
    <a href="index.html">Volver al Inicio</a>
</body>
</html>