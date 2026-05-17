export type Offer = {
  id: string;
  quantity: number;
  price: number;
  label: string;
  badge?: string;
};

export const products = [
  {
    id: "khafeefa-waist-fan-powerbank",
    slug: "waist-fan-powerbank",
    brand: "خفيفة",
    title: "مروحة خفيفة: تبريد فوري وباور بانك",
    cardTitle: "مروحة خفيفة المزدوجة",
    subtitle:
      "هواء قريب منك + شحن للطوارئ في جهاز واحد، مصمم لمشاوير الكويت والحر اليومي.",
    currency: "KWD",
    offers: [
      { 
        id: "one", 
        quantity: 1, 
        price: 12.9, 
        label: "حبة وحدة",
        badge: "للتجربة"
      },
      {
        id: "two",
        quantity: 2,
        price: 22.0,
        label: "حبتين (لك وللأهل)",
        badge: "الأكثر طلباً"
      },
      {
        id: "three",
        quantity: 3,
        price: 29.5,
        label: "٣ حبات (عرض الدوانية)",
        badge: "توفير قوي"
      }
    ]
  }
] as const;

export const formatKwd = (price: number) => `${price.toFixed(3)} د.ك`;
