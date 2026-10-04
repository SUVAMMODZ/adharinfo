export default async function handler(req, res) {

  // ✅ CORS
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "*");

  if (req.method === "OPTIONS") {
    return res.status(200).end();
  }

  const { key, term } = req.query;

  // 🔐 API KEY
  if (key !== "mynkpapa00") {
    return res.status(401).json({
      success: false,
      message: "Invalid API Key"
    });
  }

  // ❌ TERM REQUIRED
  if (!term) {
    return res.status(400).json({
      success: false,
      message: "term required"
    });
  }

  try {

    // 🔥 BACKEND API
    const response = await fetch(
      `https://users-xinfo-admin-eight.vercel.app/api?key=lljeliye&type=adhar&term=${term}`
    );

    const data = await response.json();

    // ✅ SAME TO SAME KEYMAPPING
    const formatted = {
      success: true,
      result: (data.result || []).map(item => ({
        id: item.id || item.id_number || "NA",
        mobile: item.mobile || item.MOBILE || "NA",
        name: item.name || item.NAME || "NA",
        father_name:
          item.father_name ||
          item.fname ||
          item.FNAME ||
          "NA",

        address:
          item.address ||
          item.ADDRESS ||
          "NA",

        alt_mobile:
          item.alt_mobile ||
          item.alt ||
          "NA",

        circle:
          item.circle ||
          "NA",

        id_number:
          item.id_number ||
          item.id ||
          "NA",

        email:
          item.email ||
          ""
      }))
    };

    // ✅ FINAL RESPONSE
    return res.status(200).json(formatted);

  } catch (err) {

    return res.status(500).json({
      success: false,
      message: "Server Error",
      error: err.message
    });

  }
}
