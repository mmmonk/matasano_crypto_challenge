## [49. CBC-MAC Message Forgery](c49.py)

Let's talk about CBC-MAC.

CBC-MAC is like this:

1. Take the plaintext P.
2. Encrypt P under CBC with key K, yielding ciphertext C.
3. Chuck all of C but the last block C[n].
4. C[n] is the MAC.

Suppose there's an online banking application, and it carries out user requests by talking to an API server over the network. Each request looks like this:

    message || IV || MAC

The message looks like this:

    from=#{from_id}&to=#{to_id}&amount=#{amount}

Now, write an API server and a web frontend for it. (NOTE: No need to get ambitious and write actual servers and web apps. Totally fine to go lo-fi on this one.) The client and server should share a secret key K to sign and verify messages.

The API server should accept messages, verify signatures, and carry out each transaction if the MAC is valid. It's also publicly exposed - the attacker can submit messages freely assuming he can forge the right MAC.

The web client should allow the attacker to generate valid messages for accounts he controls. (Feel free to sanitize params if you're feeling anal-retentive.) Assume the attacker is in a position to capture and inspect messages from the client to the API server.

One thing we haven't discussed is the IV. Assume the client generates a per-message IV and sends it along with the MAC. That's how CBC works, right?

Wrong.

For messages signed under CBC-MAC, an attacker-controlled IV is a liability. Why? Because it yields full control over the first block of the message.

Use this fact to generate a message transferring 1M spacebucks from a target victim's account into your account.

I'll wait. Just let me know when you're done.

... waiting

... waiting

... waiting

All done? Great - I knew you could do it!

Now let's tune up that protocol a little bit.

As we now know, you're supposed to use a fixed IV with CBC-MAC, so let's do that. We'll set ours at 0 for simplicity. This means the IV comes out of the protocol:

    message || MAC

Pretty simple, but we'll also adjust the message. For the purposes of efficiency, the bank wants to be able to process multiple transactions in a single request. So the message now looks like this:

    from=#{from_id}&tx_list=#{transactions}

With the transaction list formatted like:

    to:amount(;to:amount)*

There's still a weakness here: the MAC is vulnerable to length extension attacks. How?

Well, the output of CBC-MAC is a valid IV for a new message.

    "But we don't control the IV anymore!"

With sufficient mastery of CBC, we can fake it.

Your mission: capture a valid message from your target user. Use length extension to add a transaction paying the attacker's account 1M spacebucks.

Hint!
This would be a lot easier if you had full control over the first block of your message, huh? Maybe you can simulate that.

Food for thought: How would you modify the protocol to prevent this?

## [50. Hashing with CBC-MAC](c50.py)

Sometimes people try to use CBC-MAC as a hash function.

This is a bad idea. Matt Green explains:

> To make a long story short: cryptographic hash functions are public functions (i.e., no secret key) that have the property of collision-resistance (it's hard to find two messages with the same hash). MACs are keyed functions that (typically) provide message unforgeability -- a very different property. Moreover, they guarantee this only when the key is secret.

Let's try a simple exercise.

Hash functions are often used for code verification. This snippet of JavaScript (with newline):

		alert('MZA who was that?');

Hashes to 296b8d7cb78a243dda4d0a61d33bbdd1 under CBC-MAC with a key of "YELLOW SUBMARINE" and a 0 IV.

Forge a valid snippet of JavaScript that alerts "Ayo, the Wu is back!" and hashes to the same value. Ensure that it runs in a browser.

Extra Credit
Write JavaScript code that downloads your file, checks its CBC-MAC, and inserts it into the DOM iff it matches the expected hash.

## [51. Compression Ratio Side-Channel Attacks](c51.py)

Internet traffic is often compressed to save bandwidth. Until recently, this included HTTPS headers, and it still includes the contents of responses.

Why does that matter?

Well, if you're an attacker with:

	1. Partial plaintext knowledge and
	2. Partial plaintext control and
	3. Access to a compression oracle

You've got a pretty good chance to recover any additional unknown plaintext.

What's a compression oracle? You give it some input and it tells you how well the full message compresses, i.e. the length of the resultant output.

This is somewhat similar to the timing attacks we did way back in set 4 in that we're taking advantage of incidental side channels rather than attacking the cryptographic mechanisms themselves.

Scenario: you are running a MITM attack with an eye towards stealing secure session cookies. You've injected malicious content allowing you to spawn arbitrary requests and observe them in flight. (The particulars aren't terribly important, just roll with it.)

So! Write this oracle:

		oracle(P) -> length(encrypt(compress(format_request(P))))

Format the request like this:

		POST / HTTP/1.1
		Host: hapless.com
		Cookie: sessionid=TmV2ZXIgcmV2ZWFsIHRoZSBXdS1UYW5nIFNlY3JldCE=
		Content-Length: ((len(P)))
		((P))

(Pretend you can't see that session id. You're the attacker.)

Compress using zlib or whatever.

Encryption... is actually kind of irrelevant for our purposes, but be a sport. Just use some stream cipher. Dealer's choice. Random key/IV on every call to the oracle.

And then just return the length in bytes.

Now, the idea here is to leak information using the compression library. A payload of "sessionid=T" should compress just a little bit better than, say, "sessionid=S".

There is one complicating factor. The DEFLATE algorithm operates in terms of individual bits, but the final message length will be in bytes. Even if you do find a better compression, the difference may not cross a byte boundary. So that's a problem.

You may also get some incidental false positives.

But don't worry! I have full confidence in you.

Use the compression oracle to recover the session id.

I'll wait.

Got it? Great.

Now swap out your stream cipher for CBC and do it again.

## [52. Iterated Hash Function Multicollisions](c52.py)

While we're on the topic of hash functions...

The major feature you want in your hash function is collision-resistance. That is, it should be hard to generate collisions, and it should be really hard to generate a collision for a given hash (aka preimage).

Iterated hash functions have a problem: the effort to generate lots of collisions scales sublinearly.

What's an iterated hash function? For all intents and purposes, we're talking about the Merkle-Damgard construction. It looks like this:

		function MD(M, H, C):
			for M[i] in pad(M):
				H := C(M[i], H)
			return H

For message M, initial state H, and compression function C.

This should look really familiar, because SHA-1 and MD4 are both in this category. What's cool is you can use this formula to build a makeshift hash function out of some spare crypto primitives you have lying around (e.g. C = AES-128).

Back on task: the cost of collisions scales sublinearly. What does that mean? If it's feasible to find one collision, it's probably feasible to find a lot.

How? For a given state H, find two blocks that collide. Now take the resulting hash from this collision as your new H and repeat. Recognize that with each iteration you can actually double your collisions by subbing in either of the two blocks for that slot.

This means that if finding two colliding messages takes 2^(b/2) work (where b is the bit-size of the hash function), then finding 2^n colliding messages only takes n\*2^(b/2) work.

Let's test it. First, build your own MD hash function. We're going to be generating a LOT of collisions, so don't knock yourself out. In fact, go out of your way to make it bad. Here's one way:

	1. Take a fast block cipher and use it as C.
	2. Make H pretty small. I won't look down on you if it's only 16 bits. Pick some initial H.
	3. H is going to be the input key and the output block from C. That means you'll need to pad it on the way in and drop bits on the way out.

Now write the function f(n) that will generate 2^n collisions in this hash function.

Why does this matter? Well, one reason is that people have tried to strengthen hash functions by cascading them together. Here's what I mean:

	1. Take hash functions f and g.
	2. Build h such that h(x) = f(x) || g(x).

The idea is that if collisions in f cost 2^(b1/2) and collisions in g cost 2^(b2/2), collisions in h should come to the princely sum of 2^((b1+b2)/2).

But now we know that's not true!

Here's the idea:

	1. Pick the "cheaper" hash function. Suppose it's f.
	2. Generate 2^(b2/2) colliding messages in f.
	3. There's a good chance your message pool has a collision in g.
	4. Find it.

And if it doesn't, keep generating cheap collisions until you find it.

Prove this out by building a more expensive (but not too expensive) hash function to pair with the one you just used. Find a pair of messages that collide under both functions. Measure the total number of calls to the collision function.

## [53. Kelsey and Schneier's Expandable Messages](c53.py)

One of the basic yardsticks we use to judge a cryptographic hash function is its resistance to second preimage attacks. That means that if I give you x and y such that H(x) = y, you should have a tough time finding x' such that H(x') = H(x) = y.

How tough? Brute-force tough. For a 2^b hash function, we want second preimage attacks to cost 2^b operations.

This turns out not to be the case for very long messages.

Consider the problem we're trying to solve: we want to find a message that will collide with H(x) in the very last block. But there are a ton of intermediate blocks, each with its own intermediate hash state.

What if we could collide into one of those? We could then append all the following blocks from the original message to produce the original H(x). Almost.

We can't do this exactly because the padding will mess things up.

What we need are expandable messages.

In the last problem we used multicollisions to produce 2^n colliding messages for n\*2^(b/2) effort. We can use the same principles to produce a set of messages of length (k, k + 2^k - 1) for a given k.

Here's how:

	- Starting from the hash function's initial state, find a collision between a single-block message and a message of 2^(k-1)+1 blocks. DO NOT hash the entire long message each time. Choose 2^(k-1) dummy blocks, hash those, then focus on the last block.
	- Take the output state from the first step. Use this as your new initial state and find another collision between a single-block message and a message of 2^(k-2)+1 blocks.
	- Repeat this process k total times. Your last collision should be between a single-block message and a message of 2^0+1 = 2 blocks.

Now you can make a message of any length in (k, k + 2^k - 1) blocks by choosing the appropriate message (short or long) from each pair.

Now we're ready to attack a long message M of 2^k blocks.

	1. Generate an expandable message of length (k, k + 2^k - 1) using the strategy outlined above.
	2. Hash M and generate a map of intermediate hash states to the block indices that they correspond to.
	3. From your expandable message's final state, find a single-block "bridge" to intermediate state in your map. Note the index i it maps to.
	4. Use your expandable message to generate a prefix of the right length such that len(prefix || bridge || M[i..]) = len(M).

The padding in the final block should now be correct, and your forgery should hash to the same value as M.

