---
file_role: canonical_surface_examples
version: 1.1.0
status: normative_examples
contracts:
  render: render.v3.12.2.yaml
  lint: lint.v4.4.2.yaml
rule: examples clarify valid realization but never override governing contracts
---

# Daily Horoscopic Devotional Surface Examples

These specimens are authoritative examples of valid output shape. Content, sources, and reference count may vary. Required contracts do not. Every devotional retains its governing quotation and primary Scripture. Standard devotional prose must remain natural when spoken aloud. Images enrich the UI surface but never carry meaning required to understand the devotional. When prayer is enabled, it follows the selected primary terminal surface and precedes Additional References and footer footnotes.

## Source Presentation in Body Prose

Composition follows `engine_core.writing_constraints.body_quote_policy`.
These paragraph fragments illustrate source use, not complete devotionals:

- Scripture: Paul asks believers to act “in the name of the Lord Jesus” ([Colossians 3:17 (NIV)](https://www.biblegateway.com/passage/?search=Colossians+3%3A17&version=NIV)). The surrounding instructions about compassion and patience show the character their actions should express.
- Attributed paraphrase: Benedict assigns periods for labor, sacred reading, and rest, and calls for moderation on account of the weak ([Rule 48](https://pressbooks.palni.org/ruleofbenedict/chapter/rb-48/)). That supports a rhythm of care attentive to the worker's strength.

The source material makes each conclusion intelligible; the attribution can move to a footer when needed for flow. A primary-anchor quotation in the body does not turn that passage into an additional supporting Scripture.

## EX-UI-STANDARD · Canonical UI Devotional

**Purpose:** Shows the ordinary reader-facing devotional.

<!-- profile: artifact_type=devotional; content_length=standard; render_target=ui; images=enabled; prayer=none -->

[IMAGE GROUP: morning light crossing a worn wooden table beside an open window]

Steady Enough for Today

> “Faith is taking the first step even when you don’t see the whole staircase.”

— [Martin Luther King Jr.](https://example.org/quote-source)

We often ask God for a map when grace offers enough light for one faithful step. Scripture does not shame our desire to understand. It teaches us that trust can move before certainty arrives. Abraham went without seeing the whole road, and the disciples followed Christ before they understood where His path would lead.

The next faithful act may be modest: making the call, offering forgiveness, resting instead of forcing an answer, or returning to work that has become discouraging. None of these actions purchases God’s favor. They are ways of walking inside the favor already given. Today does not require mastery of the staircase. It asks for attention to the step beneath your feet.

[Hebrews 11:8 (NIV)](https://example.org/scripture)

Additional References

- [Psalm 119:105 (NIV)](https://example.org/psalm)
- [Proverbs 3:5–6 (NIV)](https://example.org/proverbs)
- John Chrysostom, *Homilies on Hebrews*

## Image Delivery

The image composer owns acquisition and fallback precedence in
`engine_core.image_selection.acquisition_fallback`. The assembler displays the
composer's delivered surface under `render.image_rendering`. Editors and
post-checks return delivery failures to the composer without choosing a fallback.

An acceptable delivered surface is either an actual displayed image or a
composer-supplied italic cue, for example:

*Two people carry a heavy basket between them along a sunlit path.*

The cue is text and must never be reported as a displayed image. Checks assess
that delivered product without requiring acquisition history. Existing image
exclusions for PDF, study guides, and images-disabled output remain in force.

## EX-UI-CONDENSED · Condensed UI Devotional

**Purpose:** An index card devotional at approximately a sixth-grade reading level, with optional generated prayer enabled. Engine core owns the body and surface contracts; the specimen does not set a universal reading level or enable prayer by default.

<!-- profile: artifact_type=devotional; content_length=condensed; render_target=ui; images=enabled; prayer=generated; reading_complexity=middle_school; title=disabled -->

[IMAGE GROUP: soft morning light on a quiet table set for today's work]

> “Never be afraid to trust an unknown future to a known God.”

— [Corrie ten Boom](https://www.crossway.org/articles/the-story-of-the-watchmaker-who-forgave-her-enemies/)

When you worry about tomorrow, you may keep making plans because it feels hard to stop. Jesus reminds us that our Father knows what we need and cares for us today. God stays with us through the questions we cannot answer, and his mercy meets us each morning. Pause to tell him one thing that worries you, then ask for help with one thing you can do today. Give that task your care, and let the other questions wait for now.

[Matthew 6:34 (NRSVUE)](https://www.biblegateway.com/passage/?search=Matthew+6%3A34&version=NRSVUE)

*Father, help me trust your care with the questions I cannot answer. Show me what I can do today, and help me do it with love.*

Additional References

- [Lamentations 3:22–23 (NRSVUE)](https://www.biblegateway.com/passage/?search=Lamentations+3%3A22-23&version=NRSVUE)
- [Brother Lawrence, *The Practice of the Presence of God*, Second Conversation](https://www.ccel.org/ccel/lawrence/practice.iii.ii.html)

## EX-UI-EXPANDED · Expanded UI Devotional

**Purpose:** Shows extended reasoning through connected Scriptures, an expanded study pool, and lived application. Engine core owns the numerical profile; this specimen illustrates its realization.

<!-- profile: artifact_type=devotional; content_length=expanded; render_target=ui; images=enabled; prayer=generated -->

[IMAGE GROUP: warm evening light on a kitchen table beside a clean cup]

What Will Need Doing Again

> “We ought not to be weary of doing little things for the love of God…”

— [Brother Lawrence, The Practice of the Presence of God, Fourth Conversation](https://books.google.com/books/about/The_Practice_of_the_Presence_of_God.html?id=WdCS0k3yeRQC)

There is a particular weariness in washing a cup you washed yesterday. You know where the stain gathers and which way to turn it beneath the water. By tomorrow it may be waiting here again. Much of life asks this of us: another meal, another explanation, another small effort to restore something that living has disturbed. Sometimes the repetition is comforting. Sometimes you stand at the sink longer than necessary, gathering yourself before the next thing. It can be difficult to see what your care accomplishes when the evidence of its accomplishment keeps disappearing.

Paul's invitation in Colossians to act “in the name of the Lord Jesus” reaches into this familiar world. His surrounding instructions concern patience, compassion, forgiveness, and the love that holds a community together. Those qualities become necessary precisely because people continue to need one another. Someone misunderstands again. Someone arrives tired again. Yesterday's patience becomes today's occasion to practice patience anew. An ordinary task can carry something of Christ's care into another person's day. The cup is clean long enough for someone to drink from it. What you did has entered a life, even after its visible traces are gone.

Yet this can become a heavy teaching if every need begins to sound like your assignment. Ephesians gives us a place to breathe before taking another responsibility into our hands. Paul begins, “For it is by grace you have been saved, through faith,” then describes the good works for which we are created in Christ ([Ephesians 2:8–10 (NIV)](https://www.biblegateway.com/passage/?search=Ephesians+2%3A8-10&version=NIV)). Grace makes our response possible. Tish Harrison Warren, in her account of waking in Liturgy of the Ordinary, describes belovedness as an identity received before the day's accomplishments. That remains true when we are slow to begin or must acknowledge that we cannot manage everything before us.

From that place, we can ask what our actions make possible for someone else. In Corinthians, Paul considers a shared meal and the different meanings it carries for the people eating it. His concern moves from personal freedom toward a neighbor's good ([1 Corinthians 10:23–33 (NIV)](https://www.biblegateway.com/passage/?search=1+Corinthians+10%3A23-33&version=NIV)). Grace received can take shape in care offered. Perhaps someone needs a practical burden lifted; perhaps company while they finish it. In Laborem Exercens, John Paul II places everyday provision within humanity's participation in the Creator's activity. Our work helps sustain a shared world, including lives whose needs and capacities differ from our own.

That attention should include the person doing the work. Benedict assigns periods for labor, sacred reading, and rest, and calls for moderation on account of the weak. These provisions in his Rule suggest a household rhythm in which a responsibility can have a defined portion and a reasonable stopping place. Someone can say they are tired, and someone else can take a turn. Receiving help may require leaving a task in another person's hands, done with their methods and their measure of care. We can learn to recognize love even when its arrangements differ from ours.

Jesus welcomes weary people to come close and learn from his gentleness. His promise, “I will give you rest,” accompanies an invitation to become his disciples ([Matthew 11:28–30 (NIV)](https://www.biblegateway.com/passage/?search=Matthew+11%3A28-30&version=NIV)). We can bring him resentment at being needed, longing to be noticed, or the wish that something would stay finished for a while. Prayer gives these feelings somewhere to be spoken honestly. We may need forgiveness for how we have spoken, courage to ask for help, or time to sit down while another person continues. Rest can begin with being present without immediately finding another way to be useful.

When you return to one small responsibility today, recognize the life around it. Someone will use this space, read these words, or be relieved that something has been remembered. You may be that someone. Offer what care is reasonably yours to give. If your heart is reluctant, bring that with you; affection sometimes grows while our hands are already at work. When your portion is done, let someone receive its goodness. Drink from the clean cup yourself. Sit where the evening light reaches the table, and allow this moment to sustain you before tomorrow asks its familiar things.

[Colossians 3:17 (NIV)](https://www.biblegateway.com/passage/?search=Colossians+3%3A17&version=NIV)

*Lord Jesus, help me recognize the lives my care touches, speak honestly about my limits, and welcome the care offered to me.*

Additional References

- [Ephesians 2:8–10 (NIV)](https://www.biblegateway.com/passage/?search=Ephesians+2%3A8-10&version=NIV)
- [1 Corinthians 10:23–33 (NIV)](https://www.biblegateway.com/passage/?search=1+Corinthians+10%3A23-33&version=NIV)
- [Matthew 11:28–30 (NIV)](https://www.biblegateway.com/passage/?search=Matthew+11%3A28-30&version=NIV)
- Benedict of Nursia, [Rule, Chapter 48](https://pressbooks.palni.org/ruleofbenedict/chapter/rb-48/)
- Tish Harrison Warren, [Liturgy of the Ordinary, “Waking”](https://www.ivpress.com/Media/Default/Downloads/Excerpts-and-Samples/4711-excerpt.pdf)
- John Paul II, [Laborem Exercens, §§24–26](https://www.vatican.va/content/john-paul-ii/en/encyclicals/documents/hf_jp-ii_enc_14091981_laborem-exercens.html)


## EX-UI-GENERATED-PRAYER · Generated Prayer

**Purpose:** Shows a generated prayer as an optional devotional surface. The prayer grows from the devotional’s thesis, primary Scripture, and pastoral motion, carries no historic or liturgical attribution, and remains outside the devotional body word count.

<!-- profile: artifact_type=devotional; content_length=standard; render_target=ui; images=enabled; prayer=generated -->

[IMAGE GROUP: a small boat tied safely beside a weathered dock before sunrise]

Held While Moving

> “Courage is not simply one of the virtues, but the form of every virtue at the testing point.”

— [C. S. Lewis](https://example.org/quote-source)

Courage often arrives without the feeling we expected. Scripture does not require a fearless heart before obedience begins. Again and again, God’s people move while still aware of danger, uncertainty, and their own limits. What steadies them is not confidence in themselves but confidence that God remains present in the movement.

Today’s faithful step may therefore feel smaller than bravery ought to feel. It may be a conversation you have postponed, a boundary spoken calmly, or one ordinary act of obedience performed while your hands still shake. Courage is not the absence of need. It is the willingness to entrust that need to God while taking the next faithful step.

[Joshua 1:9 (NIV)](https://example.org/scripture)

God of steady presence, meet me in the step I am afraid to take. Keep me from confusing courage with self-sufficiency. Give me enough light for faithful action, enough humility to receive help, and enough trust to move with You rather than waiting to feel invulnerable. Amen.

Additional References

- [Psalm 56:3–4 (NIV)](https://example.org/psalm56)
- [2 Timothy 1:7 (NIV)](https://example.org/timothy)

## EX-UI-LITURGICAL-PRAYER · Date-Specific Liturgical Prayer

**Purpose:** Shows a liturgical prayer as an optional surface. The prayer follows the church calendar rather than being rewritten to echo the devotional theme. Its tradition and source are identified. This specimen demonstrates shape only; production use still requires verified date appropriateness, provenance, and permission for verbatim text.

<!-- profile: artifact_type=devotional; content_length=standard; render_target=ui; images=enabled; prayer=liturgical; tradition=anglican -->

[IMAGE GROUP: late-summer sunlight falling through church windows onto an open prayer book]

The Grace of Being Sent

> “The place God calls you to is the place where your deep gladness and the world’s deep hunger meet.”

— [Frederick Buechner](https://example.org/quote-source)

Christian vocation is rarely a single hidden answer waiting to be uncovered. More often it is discerned through the gifts already given, the needs actually before us, and the relationships in which love becomes concrete. Scripture’s language of calling repeatedly turns outward. Grace gathers us, forms us, and then sends us toward the good of another.

That means today’s calling may be less mysterious than it feels. Attend to the work that asks for faithfulness now. Notice where compassion and capacity meet. Ask what love requires in the place where you already stand. A life of vocation is built from many such acts of response, each one becoming part of a larger yes.

[Ephesians 2:10 (NRSVUE)](https://example.org/scripture)

[VERIFIED DATE-SPECIFIC LITURGICAL PRAYER TEXT]

— [Proper or Collect name], Anglican tradition, [verified source](https://example.org/liturgical-source)

Additional References

- [1 Peter 4:10 (NRSVUE)](https://example.org/peter)
- [Micah 6:8 (NRSVUE)](https://example.org/micah)
- Augustine, *Confessions*

**Fallback note:** If a suitable date-specific prayer cannot be established with reliable provenance, or verbatim use is not permitted, this surface becomes a generated prayer instead. The fallback must be classified and rendered as generated, with no liturgical source attribution.

## EX-UI-MINIMAL-LINEAGE · Minimal Source Lineage

**Purpose:** Proves that the visible bibliography is not padded to a recurring total. The Scriptural Primacy composition contract still applies.

<!-- profile: artifact_type=devotional; content_length=standard; render_target=ui; images=enabled; lineage=minimal; prayer=none -->

[IMAGE GROUP: one weathered cup resting beside a quiet window]

The Grace of Enough

> “The ability to simplify means to eliminate the unnecessary so that the necessary may speak.”

— [Hans Hofmann](https://example.org/quote-source)

Much of our weariness comes from treating every concern as equally urgent. Jesus restores proportion. One thing is necessary, not because other duties are worthless, but because they find their proper shape only when attention returns to God. Simplicity begins as reordered love before it becomes an uncluttered calendar.

Today, enough may look smaller than ambition prefers. Complete the faithful task that is yours. Release the performance meant only to prove your worth. Receive ordinary bread with gratitude. The life of grace is not built by making everything important. It grows as the necessary is allowed to speak.

[Luke 10:41–42 (NIV)](https://example.org/scripture)

Additional References

- [Psalm 131:1–2 (NIV)](https://example.org/psalm)

## EX-UI-EXTENSIVE-LINEAGE · Extensive Source Lineage

**Purpose:** Proves that a larger source block is valid when each source materially shaped the devotional. It does not establish a preferred count.

<!-- profile: artifact_type=devotional; content_length=standard; render_target=ui; images=enabled; lineage=extensive; prayer=none -->

[IMAGE GROUP: many streams joining a broad river beneath cedar trees]

Many Gifts, One River

> “We are caught in an inescapable network of mutuality.”

— [Martin Luther King Jr.](https://example.org/quote-source)

The church is not a gathering of self-sufficient people who occasionally cooperate. Paul describes a body whose members receive different gifts precisely so that grace can travel between them. Dependence is not a defect left behind by maturity. It is one of the forms Christian maturity takes.

This frees us both to offer and to receive. We need not diminish another person’s gift to make room for our own, nor hide our need in order to appear useful. Christ remains the source; each person becomes one channel among many. The river is fuller because no single stream is asked to be the whole watershed.

[1 Corinthians 12:12–14 (NIV)](https://example.org/scripture)

Additional References

- [Romans 12:4–6 (NIV)](https://example.org/romans)
- [Ephesians 4:15–16 (NIV)](https://example.org/ephesians)
- [1 Peter 4:10 (NIV)](https://example.org/peter)
- Ignatius of Antioch, *Letter to the Ephesians*
- John Chrysostom, *Homilies on First Corinthians*
- Dietrich Bonhoeffer, *Life Together*
- Lesslie Newbigin, *The Household of God*

## EX-STUDY-GUIDE · Optional Study Guide

**Purpose:** Shows the separate companion artifact. It contains no image surface and does not masquerade as the devotional itself.

<!-- profile: artifact_type=study_guide; content_length=standard; render_target=ui; images=disabled -->

# Study Guide: The Work Beneath the Soil

## Governing Question

How does biblical patience differ from passivity, resignation, or loyalty to an unchanged plan?

## Primary Quotation

> “Adopt the pace of nature: her secret is patience.”

— Ralph Waldo Emerson

## Anchor Scripture

[James 5:7–8 (NIV)](https://example.org/scripture)

Read the surrounding paragraph and notice that James connects patience with strengthening the heart. Waiting is presented as a practiced posture under pressure, not empty delay.

## Scriptural Synthesis

- [Mark 4:26–29 (NIV)](https://example.org/mark): growth may be real before it becomes explainable or visible.
- [Romans 5:3–5 (NIV)](https://example.org/romans): endurance participates in the formation of character and hope.
- [Galatians 6:9 (NIV)](https://example.org/galatians): perseverance remains joined to doing good rather than mere duration.

## Historical Witness

John Chrysostom treats endurance as active fidelity shaped by hope. Pierre Teilhard de Chardin emphasizes trust in the slow work of God. Neither source governs the interpretation; both help name dimensions already present in Scripture.

## Reflection

1. Where are you tempted to interpret hidden growth as no growth?
2. What faithful work belongs to you in this season?
3. What part of the timetable needs to be released?

## Practice

Choose one small act of tending that can be completed today without demanding evidence of immediate results.

## Prayer

God of seedtime and harvest, steady my hands for faithful work and teach my heart to trust what I cannot yet see. Amen.

## Sources Used

- [James 5:7–8 (NIV)](https://example.org/scripture)
- [Mark 4:26–29 (NIV)](https://example.org/mark)
- [Romans 5:3–5 (NIV)](https://example.org/romans)
- [Galatians 6:9 (NIV)](https://example.org/galatians)
- John Chrysostom, *Homilies on the Epistle to the Romans*
- Pierre Teilhard de Chardin, “Patient Trust”

## EX-PDF-DEVOTIONAL · PDF Devotional Export

**Purpose:** Shows the print-safe devotional surface. It contains no images, entities, image cues, or UI-only components.

<!-- profile: artifact_type=devotional; content_length=standard; render_target=pdf; images=disabled; entities=disabled; prayer=none -->

**Steady Enough for Today**

> “Faith is taking the first step even when you don’t see the whole staircase.”

Martin Luther King Jr.

We often ask God for a map when grace offers enough light for one faithful step. Scripture does not shame our desire to understand. It teaches us that trust can move before certainty arrives. Abraham went without seeing the whole road, and the disciples followed Christ before they understood where His path would lead.

The next faithful act may be modest: making the call, offering forgiveness, resting instead of forcing an answer, or returning to work that has become discouraging. None of these actions purchases God’s favor. They are ways of walking inside the favor already given. Today does not require mastery of the staircase. It asks for attention to the step beneath your feet.

**Hebrews 11:8 (NIV)**

“By faith Abraham obeyed when he was called to go out to a place that he was to receive as an inheritance; and he set out, not knowing where he was going.”

## Additional References

- Psalm 119:105 (NIV)
- Proverbs 3:5–6 (NIV)
- John Chrysostom, *Homilies on Hebrews*

