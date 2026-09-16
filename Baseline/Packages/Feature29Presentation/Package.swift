// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature29Presentation",
    products: [.library(name: "Feature29Presentation", targets: ["Feature29Presentation"])],
    dependencies: [.package(path: "../Feature29Domain"),
        .package(path: "../Feature29Data")],
    targets: [.target(name: "Feature29Presentation", dependencies: [.product(name: "Feature29Domain", package: "Feature29Domain"), .product(name: "Feature29Data", package: "Feature29Data")])]
)
