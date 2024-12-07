<!DOCTYPE html>
<html>
<head>
    <title>Ranking de Brawlers por Trofeos</title>
    <link rel="stylesheet" href="styles2.css">
</head>
<body>
    <?php
    try {
        $pdo = new PDO('pgsql:host=localhost;port=5432;dbname=cc3201', 'webuser', '12brawl13');
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

        $stmt = $pdo->prepare("
            SELECT
                b.nombre_brawler AS brawler,
                SUM(t.trofeos_totales) AS trofeos_totales
            FROM
                ProyectBrawlStars.Trofeos_200_Brawler t
            JOIN
                ProyectBrawlStars.Brawler b ON t.nombre_brawler = b.nombre_brawler
            GROUP BY
                b.nombre_brawler
            ORDER BY
                trofeos_totales DESC;
        ");

        $stmt->execute();
        $result = $stmt->fetchAll(PDO::FETCH_ASSOC);

        echo "<h3>Ranking de Brawlers por Trofeos</h3>";
        echo "<table>
                <tr>
                    <th>Brawler</th>
                    <th>Trofeos Totales</th>
                </tr>";

        if (count($result) > 0) {
            foreach ($result as $row) {
                echo "<tr>
                        <td>" . htmlspecialchars($row['brawler']) . "</td>
                        <td>" . htmlspecialchars($row['trofeos_totales']) . "</td>
                      </tr>";
            }
        } else {
            echo "<tr><td colspan='2'>No se encontraron datos para los brawlers.</td></tr>";
        }
        echo "</table>";
    } catch (PDOException $e) {
        echo "Error: " . $e->getMessage();
    }
    ?>
    <a href="index.html">Volver al Inicio</a>
</body>
</html>