import Link from "next/link";
import { OfferCard } from "@/components/offer-card";
import { SiteFooter } from "@/components/site-footer";
import { SiteHeader } from "@/components/site-header";
import { CheckoutForm } from "@/components/checkout-form";
import { products } from "@/data/products";

const product = products[0];

const proofBadges = [
  "دفع عند الاستلام",
  "مناسب لمشاوير الكويت",
  "ضمان استرجاع ٧ أيام",
  "باور بانك للطوارئ"
];

export default function Home() {
  return (
    <>
      <SiteHeader />
      <main>
        <section className="overflow-hidden bg-[linear-gradient(135deg,var(--warm-cream),var(--sand))] py-16 md:py-24">
          <div className="container grid items-center gap-12 md:grid-cols-2">
            <div className="order-2 md:order-1 space-y-8">
              <div className="inline-flex rounded-full border border-[var(--border)] bg-white/70 px-4 py-2 text-sm font-bold text-[var(--khafeefa-olive)]">
                إطلاق خفيفة الأول داخل الكويت
              </div>
              <div className="space-y-5">
                <h1 className="text-4xl font-black leading-tight text-[var(--ink)] md:text-6xl">
                  {product.title}
                </h1>
                <p className="max-w-xl text-lg leading-9 text-[var(--muted)]">
                  راحة لا تضاهى، وطاقة لا تنقطع - رفيقك الأساسي في حر الصيف.
                </p>
                <p className="max-w-xl text-lg leading-9 text-[var(--muted)]">
                  {product.subtitle}
                </p>
              </div>
              <div className="flex flex-col gap-3 sm:flex-row">
                <a
                  href="#offers"
                  className="rounded-full bg-[var(--cta-orange)] px-8 py-4 text-center text-lg font-black text-white shadow-lg"
                >
                  اختار العرض واطلب
                </a>
                <a
                  href="#offers"
                  className="rounded-full border border-[var(--border)] bg-white px-8 py-4 text-center text-lg font-bold text-[var(--date-brown)]"
                >
                  شوف الأسعار
                </a>
              </div>
              <div className="grid grid-cols-2 gap-3 text-sm font-bold text-[var(--date-brown)] sm:grid-cols-4">
                {proofBadges.map((badge) => (
                  <div key={badge} className="rounded-2xl bg-white/75 p-3 text-center">
                    {badge}
                  </div>
                ))}
              </div>
            </div>
            <div className="order-1 md:order-2 relative">
              <div className="absolute inset-8 rounded-full bg-[var(--cool-mint)] blur-3xl" />
              <div className="relative rounded-[2rem] border border-white/80 bg-white/65 p-6 shadow-2xl">
                <div className="grid min-h-[420px] place-items-center rounded-[1.5rem] bg-[radial-gradient(circle_at_50%_20%,#ffffff,#d8e7de_45%,#5a6b42)] p-8 text-center">
                  <div className="space-y-4">
                    <p className="text-7xl">❋</p>
                    <p className="text-2xl font-black text-white drop-shadow">
                      صورة المنتج البديلة
                    </p>
                    <p className="mx-auto max-w-xs text-sm leading-7 text-white/90">
                      مساحة جاهزة لاستبدالها بصورة مروحة الخصر مع العبوة الخاصة
                      بخفيفة.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section id="offers" className="py-16">
          <div className="container space-y-8">
            <div className="max-w-2xl space-y-3">
              <div className="flex items-center gap-3">
                <p className="font-bold text-[var(--khafeefa-olive)]">العروض</p>
                <span className="rounded-full bg-[var(--trust-green)]/10 px-3 py-1 text-xs font-bold text-[var(--trust-green)]">
                  ضمان استرجاع ٧ أيام
                </span>
              </div>
              <h2 className="text-3xl font-black md:text-4xl">
                توصيل مجاني، الدفع عند الاستلام
              </h2>
              <p className="leading-8 text-[var(--muted)]">
                اختر العرض المناسب لك أو للعائلة. الدفع عند الاستلام داخل الكويت لضمان حقك وتجربتك للمنتج، مع ضمان استرجاع كامل المبلغ خلال ٧ أيام إذا لم يعجبك.
              </p>
            </div>
            <div className="grid gap-4 md:grid-cols-3">
              {product.offers.map((offer) => (
                <OfferCard key={offer.id} offer={offer} />
              ))}
            </div>
          </div>
        </section>

        <section className="bg-white/55 py-16">
          <div className="container grid gap-8 md:grid-cols-3">
            {[
              ["خفيفة في اللبس", "تثبت على الخصر أو الحزام لتبقى يداك حرة."],
              ["عملية في الحر", "هواء قريب منك أثناء المشي والانتظار والمشاوير."],
              ["شحن للطوارئ", "باور بانك مدمج لاستخدامات الهاتف الضرورية."]
            ].map(([title, text]) => (
              <article
                key={title}
                className="rounded-3xl border border-[var(--border)] bg-[var(--warm-cream)] p-6"
              >
                <h3 className="text-xl font-black">{title}</h3>
                <p className="mt-3 leading-8 text-[var(--muted)]">{text}</p>
              </article>
            ))}
          </div>
        </section>

        <section className="py-16 md:py-24">
          <div className="container grid items-center gap-12 md:grid-cols-2">
            <div className="order-2 md:order-1 relative">
              <div className="absolute inset-8 rounded-full bg-[var(--sand)] blur-3xl" />
              <div className="relative rounded-[2rem] border border-[var(--border)] bg-white p-4 shadow-xl">
                <div className="grid min-h-[500px] place-items-center rounded-[1.5rem] bg-[var(--warm-cream)] p-8 text-center">
                  <div className="space-y-4">
                    <p className="text-7xl">📸</p>
                    <p className="text-xl font-black text-[var(--ink)]">
                      صورة تفاصيل المنتج
                    </p>
                    <p className="mx-auto max-w-xs text-sm leading-7 text-[var(--muted)]">
                      مساحة مخصصة لصورة توضح تفاصيل مروحة الخصر، مثل طريقة التثبيت، أزرار التحكم، ومنافذ الشحن.
                    </p>
                  </div>
                </div>
              </div>
            </div>
            <div className="order-1 md:order-2 space-y-8">
              <div className="space-y-4">
                <h2 className="text-3xl font-black md:text-4xl text-[var(--ink)]">
                  تصميم ذكي يخدمك في كل مشوار
                </h2>
                <p className="text-lg leading-8 text-[var(--muted)]">
                  صممنا "خفيفة" لتكون رفيقك المثالي في الأجواء الحارة. بفضل تصميمها المدمج وقوة أدائها، توفر لك راحة فورية أينما كنت.
                </p>
              </div>
              
              <ul className="space-y-6">
                {[
                  {
                    title: "مشبك مزدوج قوي",
                    desc: "تثبيت آمن على الحزام أو البنطلون من الداخل والخارج لضمان عدم سقوطها أثناء الحركة."
                  },
                  {
                    title: "٣ مستويات للسرعة",
                    desc: "تحكم كامل بقوة الهواء بضغطة زر واحدة لتناسب احتياجك في مختلف الأوقات."
                  },
                  {
                    title: "بطارية تدوم طويلاً",
                    desc: "سعة بطارية كبيرة تكفي لساعات من التبريد المستمر، مع إمكانية شحن هاتفك عند الحاجة."
                  }
                ].map((feature, idx) => (
                  <li key={idx} className="flex gap-4">
                    <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-[var(--cool-mint)] text-[var(--khafeefa-olive)] font-bold">
                      {idx + 1}
                    </div>
                    <div>
                      <h4 className="font-bold text-[var(--ink)] text-lg">{feature.title}</h4>
                      <p className="mt-1 text-[var(--muted)] leading-7">{feature.desc}</p>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </section>

        <section className="py-16 bg-[var(--sand)]">
          <div className="container space-y-10">
            <div className="text-center space-y-3">
              <h2 className="text-3xl font-black md:text-4xl">
                تجارب عملائنا
              </h2>
              <p className="text-[var(--muted)]">
                آراء حقيقية من أشخاص جربوا خفيفة في مشاويرهم
              </p>
            </div>
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
              {[
                {
                  name: "عبدالله المطيري",
                  text: "فكت أزمة بالصيف! خفيفة على الخصر والهوا قوي، والباور بانك ينقذ وقت الحاجة.",
                  rating: 5,
                  date: "قبل يومين"
                },
                {
                  name: "خالد الكندري",
                  text: "ممتازة حق الدوام الميداني والمشاوير، بطاريتها تطول وتبرد عليك بشكل ملحوظ.",
                  rating: 5,
                  date: "قبل أسبوع"
                },
                {
                  name: "أم فهد",
                  text: "شريت العرض بو قطعتين لي ولولدي، جودتها ممتازة وتستاهل سعرها بصراحة.",
                  rating: 5,
                  date: "قبل أسبوعين"
                },
                {
                  name: "يوسف العازمي",
                  text: "فكرتها ذكية، الهوا يضرب بالجسم مباشرة وتريحك من الحر، انصح فيها بشدة.",
                  rating: 4,
                  date: "قبل شهر"
                }
              ].map((review, i) => (
                <div key={i} className="rounded-2xl bg-white p-6 shadow-sm border border-[var(--border)] space-y-4">
                  <div className="flex items-center justify-between">
                    <div className="font-bold text-[var(--ink)]">{review.name}</div>
                    <div className="flex text-[var(--cta-orange)]">
                      {Array.from({ length: 5 }).map((_, j) => (
                        <svg key={j} className={`w-4 h-4 ${j < review.rating ? "fill-current" : "fill-gray-200"}`} viewBox="0 0 20 20">
                          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                        </svg>
                      ))}
                    </div>
                  </div>
                  <p className="text-sm leading-7 text-[var(--muted)]">"{review.text}"</p>
                  <div className="text-xs text-gray-400">{review.date}</div>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className="py-16 bg-white">
          <div className="container max-w-4xl space-y-10">
            <div className="text-center space-y-3">
              <h2 className="text-3xl font-black md:text-4xl text-[var(--ink)]">
                أسئلة شائعة
              </h2>
              <p className="text-[var(--muted)]">
                كل اللي تحتاج تعرفه عن خفيفة وتجربة الشراء
              </p>
            </div>
            <div className="grid gap-4 md:grid-cols-2">
              {[
                {
                  q: "كم ياخذ وقت التوصيل؟",
                  a: "التوصيل سريع جداً داخل الكويت، يوصلك الطلب لغاية باب بيتك خلال ٢٤ إلى ٤٨ ساعة كحد أقصى."
                },
                {
                  q: "شلون طريقة الدفع؟",
                  a: "عشان تكون متطمن، وفرنا لك الدفع عند الاستلام. ما تدفع ولا شيء لين يوصلك المندوب وتستلم طلبك بيدك."
                },
                {
                  q: "في ضمان على المنتج؟",
                  a: "أكيد! نوفر لك ضمان استرجاع كامل المبلغ خلال ٧ أيام من استلام الطلب إذا ما ناسبك المنتج لأي سبب."
                },
                {
                  q: "كم تقعد بطارية المروحة؟",
                  a: "البطارية مصممة تكفي مشاويرك اليومية وتدوم لساعات حسب سرعة الهواء، وتقدر تستخدمها كباور بانك لشحن تلفونك وقت الطوارئ."
                },
                {
                  q: "هل المروحة ثقيلة باللبس؟",
                  a: "أبداً، اسم على مسمى! تصميمها خفيف جداً ومدروس عشان يكون مريح وما يضايقك أثناء المشي أو الحركة."
                },
                {
                  q: "تركب على أي لبس؟",
                  a: "نعم، المروحة مزودة بمشبك مزدوج قوي يثبت بسهولة على الحزام أو البنطلون من الداخل والخارج لضمان ثباتها."
                }
              ].map((faq, i) => (
                <div key={i} className="rounded-2xl border border-[var(--border)] bg-[var(--warm-cream)] p-6">
                  <h3 className="font-bold text-[var(--ink)] text-lg">{faq.q}</h3>
                  <p className="mt-2 text-[var(--muted)] leading-7">{faq.a}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section id="checkout" className="py-16 md:py-24 bg-white">
          <div className="container max-w-2xl">
            <CheckoutForm />
          </div>
        </section>

        <section id="contact" className="py-16 bg-[var(--sand)]">
          <div className="container max-w-3xl text-center space-y-8">
            <div className="space-y-3">
              <h2 className="text-3xl font-black md:text-4xl text-[var(--ink)]">
                تواصل معانا
              </h2>
              <p className="text-lg text-[var(--muted)]">
                فريقنا المميز موجود عشانك! إذا عندك أي استفسار أو مشكلة، لا تتردد تكلمنا.
              </p>
            </div>
            
            <div className="grid gap-6 sm:grid-cols-2">
              <a 
                href="https://wa.me/96500000000" 
                target="_blank" 
                rel="noopener noreferrer"
                className="flex flex-col items-center gap-4 rounded-3xl border border-[var(--border)] bg-white p-8 transition-transform hover:-translate-y-1 hover:shadow-lg"
              >
                <div className="flex h-16 w-16 items-center justify-center rounded-full bg-[#25D366]/10 text-[#25D366]">
                  <svg className="h-8 w-8" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51a12.8 12.8 0 00-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
                  </svg>
                </div>
                <div>
                  <h3 className="font-bold text-[var(--ink)] text-xl">واتساب</h3>
                  <p className="mt-1 text-[var(--muted)]">رد سريع خلال ساعات العمل</p>
                </div>
              </a>
              
              <a 
                href="mailto:support@khafeefa.com" 
                className="flex flex-col items-center gap-4 rounded-3xl border border-[var(--border)] bg-white p-8 transition-transform hover:-translate-y-1 hover:shadow-lg"
              >
                <div className="flex h-16 w-16 items-center justify-center rounded-full bg-[var(--cta-orange)]/10 text-[var(--cta-orange)]">
                  <svg className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                </div>
                <div>
                  <h3 className="font-bold text-[var(--ink)] text-xl">البريد الإلكتروني</h3>
                  <p className="mt-1 text-[var(--muted)]">support@khafeefa.com</p>
                </div>
              </a>
            </div>
          </div>
        </section>
      </main>
      <SiteFooter />
    </>
  );
}
