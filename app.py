import React, { useState } from 'react';
import { Search, Sparkles, Brain, TrendingUp } from 'lucide-react';

const PasabahceAnalyzer = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [analyzedProducts, setAnalyzedProducts] = useState({});
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  // Simüle edilmiş ürün veritabanı
  const SAMPLE_PRODUCTS = {
    "Bella Vazo": {
      url: "https://www.pasabahcemagazalari.com/bella-vazo",
      rawStory: "Bella, zamanın özenle işlediği cam sanatının bir eseridir. Her detayı, ustalık ve estetiğin birleşimidir.",
      image: "https://images.unsplash.com/photo-1578749556568-bc2c40e68b61?w=400"
    },
    "Lykia Kase": {
      url: "https://www.pasabahcemagazalari.com/lykia-kase",
      rawStory: "Antik Lykia medeniyetinden ilham alan bu kase, geçmişin izlerini günümüze taşır.",
      image: "https://images.unsplash.com/photo-1610701596007-11502861dcfa?w=400"
    },
    "Diva Kadeh": {
      url: "https://www.pasabahcemagazalari.com/diva-kadeh",
      rawStory: "Her yudum, bir ritüeldir. Diva, sofranızın baş tacıdır.",
      image: "https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?w=400"
    }
  };

  const analyzeProduct = async (productName, rawStory) => {
    setIsAnalyzing(true);
    
    // API çağrısı simülasyonu
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    const analysis = {
      allegory: `${productName}, zamanın kristalleşmiş iradesidir. Her yüzeyi, bilinçaltının geometrik tezahürüdür. Maddenin içinde saklı olan formların özgürleşme anıdır. Bu nesne, kullanıcısına "Ben buradayım" diyen sessiz bir manifestodur. Cam, ışığı sadece geçirmeyi değil, dönüştürmeyi de bilir—tıpkı insan bilincinin ham deneyimleri anlamlara dönüştürmesi gibi.`,
      
      mnemonics: [
        `${productName} = Zamanın Maddeleşmiş Belleği`,
        "Her kullanım, nöral yolları güçlendirir (Hebbian İlkesi)",
        "Sahiplik değil, vekillik: Siz bu eserin koruyucususunuz"
      ],
      
      salesTips: [
        {
          title: "Nesne Kalıcılığı Prensibi",
          content: `${productName}, müşterinizin mekanında kalıcı bir 'yer işareti' oluşturur. Psikolojide 'nesne sürekliliği' olarak bilinen bu fenomen, mekana aidiyet duygusunu %67 artırır. Her bakış, ev sahibinin estetik kimliğini pekiştirir.`
        },
        {
          title: "Estetik Ödül Mekanizması",
          content: "Beynin ödül merkezi (nucleus accumbens), simetrik ve dengeli formları gördüğünde dopamin salgılar. Bu ürün, günlük hayatta 'mikro-mutluluk' kaynağıdır. Sabah kahveniz bile bir ritüele dönüşür."
        },
        {
          title: "Sosyal Sinyal Teorisi",
          content: "Ev ziyaretlerinde, seçkin nesneler 'kültürel sermaye' işlevi görür. Bu, sahibinin kimliğini iletişim kurmadan ifade eder (Bourdieu, 1984). Misafirleriniz sizi anlamadan hisseder."
        }
      ]
    };
    
    setIsAnalyzing(false);
    return analysis;
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) return;
    
    const matches = Object.entries(SAMPLE_PRODUCTS).filter(([name]) =>
      name.toLowerCase().includes(searchQuery.toLowerCase())
    );
    
    const newAnalyzed = {};
    
    for (const [name, data] of matches) {
      const cacheKey = `${name}_${data.rawStory.substring(0, 50)}`;
      
      if (analyzedProducts[cacheKey]) {
        newAnalyzed[cacheKey] = analyzedProducts[cacheKey];
      } else {
        const analysis = await analyzeProduct(name, data.rawStory);
        newAnalyzed[cacheKey] = { ...data, name, analysis };
      }
    }
    
    setAnalyzedProducts(newAnalyzed);
  };

  const filteredProducts = Object.entries(SAMPLE_PRODUCTS).filter(([name]) =>
    name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white p-6">
      {/* Header */}
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-5xl font-light tracking-widest text-amber-400 mb-3">
            ⚱️ ALEGORİK ÜRÜN İSTİHBARAT SİSTEMİ ⚱️
          </h1>
          <p className="text-amber-400/70 text-sm tracking-[0.3em]">
            MUTLAK DOĞRU ARŞİVİ
          </p>
        </div>

        {/* Search Bar */}
        <div className="max-w-2xl mx-auto mb-12">
          <div className="relative">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
              placeholder="Ürün adı yazınız (örn: Bella, Lykia, Diva)..."
              className="w-full bg-white/10 backdrop-blur-md border-2 border-amber-400/50 rounded-xl px-6 py-4 text-lg focus:outline-none focus:border-amber-400 transition-all"
            />
            <button
              onClick={handleSearch}
              className="absolute right-3 top-1/2 -translate-y-1/2 bg-amber-400 text-slate-900 p-3 rounded-lg hover:bg-amber-300 transition-all"
            >
              <Search size={20} />
            </button>
          </div>
        </div>

        {/* Results */}
        {isAnalyzing && (
          <div className="text-center text-amber-400 mb-8">
            <Sparkles className="inline animate-spin mr-2" />
            Analiz ediliyor...
          </div>
        )}

        {Object.entries(analyzedProducts).map(([key, product]) => (
          <div
            key={key}
            className="bg-white/5 backdrop-blur-lg border border-amber-400/30 rounded-2xl p-8 mb-8 hover:border-amber-400/50 transition-all"
          >
            <div className="flex gap-6 mb-6">
              <img
                src={product.image}
                alt={product.name}
                className="w-48 h-48 object-cover rounded-lg border-2 border-amber-400/30"
              />
              <div className="flex-1">
                <h2 className="text-3xl font-light text-amber-400 mb-3">
                  {product.name}
                </h2>
                <a
                  href={product.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-400 hover:text-blue-300 transition-colors"
                >
                  🔗 Ürün Sayfası
                </a>
              </div>
            </div>

            {/* Allegory */}
            <div className="mb-6">
              <div className="flex items-center gap-2 mb-3 border-b border-amber-400/30 pb-2">
                <Sparkles className="text-amber-400" size={20} />
                <h3 className="text-xl font-semibold text-amber-400">
                  Derin Alegori
                </h3>
              </div>
              <p className="text-gray-200 leading-relaxed italic text-justify">
                {product.analysis.allegory}
              </p>
            </div>

            {/* Mnemonics */}
            <div className="mb-6">
              <div className="flex items-center gap-2 mb-3 border-b border-amber-400/30 pb-2">
                <Brain className="text-amber-400" size={20} />
                <h3 className="text-xl font-semibold text-amber-400">
                  Mnemoni (Hafıza Çivileri)
                </h3>
              </div>
              <div className="space-y-3">
                {product.analysis.mnemonics.map((mnem, idx) => (
                  <div
                    key={idx}
                    className="bg-amber-400/10 border-l-4 border-amber-400 p-4 rounded"
                  >
                    {mnem}
                  </div>
                ))}
              </div>
            </div>

            {/* Sales Tips */}
            <div>
              <div className="flex items-center gap-2 mb-3 border-b border-amber-400/30 pb-2">
                <TrendingUp className="text-amber-400" size={20} />
                <h3 className="text-xl font-semibold text-amber-400">
                  Klinik Satış Tiyoları
                </h3>
              </div>
              <div className="space-y-4">
                {product.analysis.salesTips.map((tip, idx) => (
                  <div
                    key={idx}
                    className="bg-purple-900/40 border border-amber-400/20 rounded-lg p-5"
                  >
                    <h4 className="font-semibold text-amber-300 mb-2">
                      {tip.title}
                    </h4>
                    <p className="text-gray-300 leading-relaxed">
                      {tip.content}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        ))}

        {searchQuery && filteredProducts.length === 0 && !isAnalyzing && (
          <div className="text-center text-gray-400 bg-white/5 rounded-xl p-8">
            🔍 Eşleşen ürün bulunamadı. Lütfen farklı bir anahtar kelime deneyin.
          </div>
        )}

        {/* Footer */}
        <div className="text-center text-gray-500 text-sm mt-16 pt-8 border-t border-gray-700">
          <p className="mb-2">
            🏺 Bu sistem, nesnelerin metafizik değerini klinik satış stratejilerine dönüştürür.
          </p>
          <p>Sarsılmazlık İlkesi: Gerçeğin Peşinde, Aldanmanın Ötesinde.</p>
        </div>
      </div>
    </div>
  );
};

export default PasabahceAnalyzer;
