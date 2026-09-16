// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature32Presentation",
    products: [.library(name: "Feature32Presentation", targets: ["Feature32Presentation"])],
    dependencies: [.package(path: "../Feature32Domain"),
        .package(path: "../Feature32Data")],
    targets: [.target(name: "Feature32Presentation", dependencies: [.product(name: "Feature32Domain", package: "Feature32Domain"), .product(name: "Feature32Data", package: "Feature32Data")])]
)
