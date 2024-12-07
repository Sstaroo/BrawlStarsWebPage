<!DOCTYPE html>
<html>
<head>
    <title>Ranking de Clubes por Trofeos</title>
    <link rel="stylesheet" href="styles2.css">
</head>
<body>
    <?php
    try {
        $pdo = new PDO('pgsql:host=localhost;port=5432;dbname=cc3201', 'webuser', '12brawl13');
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

        $stmt = $pdo->prepare("
            SELECT
                c.nombre_club AS club,
                SUM(r.trofeos) AS trofeos_totales,
                c.nombre_pais AS pais
            FROM
                ProyectBrawlStars.Ranking_Club_Pais r
            JOIN
                ProyectBrawlStars.Club c ON r.tag_club = c.tag_club
            GROUP BY
                c.nombre_club, c.nombre_pais
            ORDER BY
                trofeos_totales DESC
            LIMIT 50;
        ");

        $stmt->execute();
        $result = $stmt->fetchAll(PDO::FETCH_ASSOC);

        echo "<h3>Ranking de Clubes por Trofeos</h3>";
        echo "<table>
                <tr>
                    <th>Club</th>
                    <th>Trofeos Totales</th>
                    <th>Pa  s</th>
                </tr>";

        if (count($result) > 0) {
            foreach ($result as $row) {
                echo "<tr>
                        <td>" . htmlspecialchars($row['club']) . "</td>
                        <td>" . htmlspecialchars($row['trofeos_totales']) . "</td>
                        <td>" . htmlspecialchars($row['pais']) . "</td>
                      </tr>";
            }
        } else {
            echo "<tr><td colspan='3'>No se encontraron datos para los clubes.</td></tr>";
        }
        echo "</table>";
    } catch (PDOException $e) {
        echo "Error: " . $e->getMessage();
    }
    ?>
    <a href="index.html">Volver al Inicio</a>
</body>
</html>