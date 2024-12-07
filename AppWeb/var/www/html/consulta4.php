<!DOCTYPE html>
<html>
<head>
    <title>Consulta: Ranking de Brawlers por Pa  s</title>
    <link rel="stylesheet" href="styles2.css">
</head>
<body>
    <?php
    try {
        $pdo = new PDO('pgsql:host=localhost;port=5432;dbname=cc3201', 'webuser', '12brawl13');
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

        if (!isset($_GET['nombre_mes']) || empty(trim($_GET['nombre_mes']))) {
            die("Error: No se proporcion   un mes v  lido.");
        }
        if (!isset($_GET['nombre_pais']) || empty(trim($_GET['nombre_pais']))) {
            die("Error: No se proporcion   un pa  s v  lido.");
        }

        $nombre_mes = trim($_GET['nombre_mes']);
        $nombre_pais = trim($_GET['nombre_pais']);

        $stmt = $pdo->prepare("
            SELECT
                p.nombre_pais,
                b.nombre_brawler,
                SUM(jc.trofeos) AS total_trofeos,
                RANK() OVER (PARTITION BY p.nombre_pais ORDER BY SUM(jc.trofeos) DESC) AS rank_brawler
            FROM
                ProyectBrawlStars.JuegaCon jc
            JOIN
                ProyectBrawlStars.Jugador j
            ON
                jc.tag_jugador = j.tag_jugador
            JOIN
                ProyectBrawlStars.Pais p
            ON
                j.nombre_pais = p.nombre_pais
            JOIN
                ProyectBrawlStars.Brawler b
            ON
                jc.nombre_brawler = b.nombre_brawler
            WHERE
                jc.nombre_mes = :Month
                AND p.nombre_pais = :Country
            GROUP BY
                p.nombre_pais, b.nombre_brawler
            ORDER BY
                rank_brawler;
        ");

        $stmt->execute([
            'Month' => $nombre_mes,
            'Country' => $nombre_pais,
        ]);
        $result = $stmt->fetchAll(PDO::FETCH_ASSOC);

        // Mostrar resultados
        echo "<h3>Resultados para el Pa  s: " . htmlspecialchars($nombre_pais) . " y Mes: " . htmlspecialchars($nombre_mes) . "</h3>";
        echo "<table>
                <tr>
                    <th>Pa  s</th>
                    <th>Brawler</th>
                    <th>Total de Trofeos</th>
                    <th>Ranking</th>
                </tr>";

        if (count($result) > 0) {
            foreach ($result as $row) {
                echo "<tr>
                        <td>" . htmlspecialchars($row['nombre_pais']) . "</td>
                        <td>" . htmlspecialchars($row['nombre_brawler']) . "</td>
                        <td>" . htmlspecialchars($row['total_trofeos']) . "</td>
                        <td>" . htmlspecialchars($row['rank_brawler']) . "</td>
                      </tr>";
            }
        } else {
            echo "<tr><td colspan='4'>No se encontraron datos para el pa  s y mes ingresados.</td></tr>";
        }
        echo "</table>";
    } catch (PDOException $e) {
        echo "Error: " . $e->getMessage();
    }
    ?>
    <a href="index.html">Volver al Inicio</a>
</body>
</html>