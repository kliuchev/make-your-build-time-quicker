import Feature31Domain

public enum Feature31DataRepository {
    public static func load(_ id: Int) -> Feature31DomainModel {
        Feature31DomainModel(id: id, title: "Feature 31")
    }
}
